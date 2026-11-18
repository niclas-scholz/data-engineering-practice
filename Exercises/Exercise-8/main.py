from pathlib import Path

import duckdb

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "Electric_Vehicle_Population_Data.csv"
PARQUET_DIR = BASE_DIR / "output" / "cars_by_model_year"

DDL = """
CREATE OR REPLACE TABLE ev_vehicles (
    vin VARCHAR,
    county VARCHAR,
    city VARCHAR,
    state VARCHAR,
    postal_code VARCHAR,
    model_year SMALLINT,
    make VARCHAR,
    model VARCHAR,
    ev_type VARCHAR,
    cafv_eligibility VARCHAR,
    electric_range SMALLINT,
    base_msrp INTEGER,
    legislative_district SMALLINT,
    dol_vehicle_id BIGINT,
    vehicle_location VARCHAR,
    electric_utility VARCHAR,
    census_tract VARCHAR
)
"""


def connect():
    return duckdb.connect()


def create_table(con):
    con.execute(DDL)


def load_csv(con, path=DATA_FILE):
    con.execute(f"COPY ev_vehicles FROM '{path}' (HEADER)")


def cars_per_city(con):
    return con.sql(
        """
        SELECT city, count(*) AS cars
        FROM ev_vehicles
        GROUP BY city
        ORDER BY cars DESC, city
        """
    ).fetchall()


def top_models(con, limit=3):
    return con.sql(
        f"""
        SELECT make, model, count(*) AS cars
        FROM ev_vehicles
        GROUP BY make, model
        ORDER BY cars DESC, make, model
        LIMIT {limit}
        """
    ).fetchall()


def most_popular_model_per_postal_code(con):
    return con.sql(
        """
        SELECT postal_code, make, model, cars
        FROM (
            SELECT
                postal_code,
                make,
                model,
                count(*) AS cars,
                row_number() OVER (
                    PARTITION BY postal_code
                    ORDER BY count(*) DESC, make, model
                ) AS rn
            FROM ev_vehicles
            GROUP BY postal_code, make, model
        )
        WHERE rn = 1
        ORDER BY postal_code
        """
    ).fetchall()


def export_cars_by_model_year(con, out_dir=PARQUET_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)
    con.execute(
        f"""
        COPY (
            SELECT model_year, count(*) AS cars
            FROM ev_vehicles
            GROUP BY model_year
        ) TO '{out_dir}' (FORMAT PARQUET, PARTITION_BY (model_year), OVERWRITE_OR_IGNORE)
        """
    )


def main():
    con = connect()
    create_table(con)
    load_csv(con)

    print("Cars per city (top 10):", cars_per_city(con)[:10])
    print("Top 3 models:", top_models(con))
    print(
        "Most popular model per postal code (top 10):",
        most_popular_model_per_postal_code(con)[:10],
    )

    export_cars_by_model_year(con)
    print(f"Parquet files written to {PARQUET_DIR}")


if __name__ == "__main__":
    main()
