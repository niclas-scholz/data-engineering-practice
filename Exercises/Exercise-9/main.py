from pathlib import Path

import polars as pl

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "202306-divvy-tripdata.csv"


def scan_rides(path=DATA_FILE):
    return pl.scan_csv(path).with_columns(
        pl.col("started_at", "ended_at").str.to_datetime("%Y-%m-%d %H:%M:%S"),
        pl.col("start_lat", "start_lng", "end_lat", "end_lng").cast(pl.Float64),
        pl.col("start_station_id", "end_station_id").cast(pl.String),
        pl.col("rideable_type", "member_casual").cast(pl.Categorical),
    )


def rides_per_day(rides):
    return (
        rides.group_by(pl.col("started_at").dt.date().alias("date")).len().sort("date")
    )


def weekly_stats(rides):
    weekly = rides.group_by(pl.col("started_at").dt.truncate("1w").alias("week")).len()
    return weekly.select(
        pl.col("len").mean().alias("avg_rides"),
        pl.col("len").max().alias("max_rides"),
        pl.col("len").min().alias("min_rides"),
    )


def day_vs_last_week(rides):
    daily = rides_per_day(rides)
    last_week = daily.select(
        (pl.col("date") + pl.duration(days=7)).alias("date"),
        pl.col("len").alias("last_week"),
    )
    return (
        daily.join(last_week, on="date", how="left")
        .select(
            "date",
            "len",
            (pl.col("len").cast(pl.Int64) - pl.col("last_week").cast(pl.Int64)).alias(
                "diff"
            ),
        )
        .sort("date")
    )


def main():
    rides = scan_rides()

    print("Rides per day:")
    print(rides_per_day(rides).collect())
    print("Weekly stats:")
    print(weekly_stats(rides).collect())
    print("Rides per day vs same day last week:")
    print(day_vs_last_week(rides).collect())


if __name__ == "__main__":
    main()
