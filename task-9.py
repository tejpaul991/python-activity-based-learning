
from statistics import mean


class BusRoutePerformanceAnalysis:

    def __init__(
        self,
        bus_capacity,
        max_journey_time,
        max_fuel_per_km,
        overload_threshold=1.0
    ):
        self.bus_capacity = bus_capacity
        self.max_journey_time = max_journey_time
        self.max_fuel_per_km = max_fuel_per_km
        self.overload_threshold = overload_threshold

        if bus_capacity <= 0:
            raise ValueError("Bus capacity must be positive.")

        if max_journey_time <= 0 or max_fuel_per_km <= 0:
            raise ValueError("Efficiency limits must be positive.")

        if overload_threshold < 1:
            raise ValueError(
                "Overload threshold must be at least 1.0."
            )

    def validate_data(self, route_data):
        if not route_data:
            raise ValueError("At least one route is required.")

        expected_days = None

        for route, daily_records in route_data.items():
            if not route.strip():
                raise ValueError("Route name cannot be empty.")

            if not daily_records:
                raise ValueError(
                    f"No daily records provided for {route}."
                )

            if expected_days is None:
                expected_days = len(daily_records)
            elif len(daily_records) != expected_days:
                raise ValueError(
                    "All routes must have the same number of days."
                )

            for day, record in enumerate(daily_records, start=1):
                required_fields = {
                    "passengers",
                    "journey_time",
                    "fuel_used",
                    "distance"
                }

                if not required_fields.issubset(record):
                    raise ValueError(
                        f"Missing data for {route}, day {day}."
                    )

                for field in required_fields:
                    value = record[field]

                    if (
                        isinstance(value, bool)
                        or not isinstance(value, (int, float))
                        or value < 0
                    ):
                        raise ValueError(
                            f"Invalid {field} for {route}, day {day}."
                        )

                if record["distance"] <= 0:
                    raise ValueError(
                        f"Distance must be positive for {route}, "
                        f"day {day}."
                    )

                if not isinstance(record["passengers"], int):
                    raise ValueError(
                        f"Passenger count must be an integer "
                        f"for {route}, day {day}."
                    )

    def analyse_route(self, daily_records):
        total_passengers = sum(
            day["passengers"] for day in daily_records
        )
        total_journey_time = sum(
            day["journey_time"] for day in daily_records
        )
        total_fuel = sum(
            day["fuel_used"] for day in daily_records
        )
        total_distance = sum(
            day["distance"] for day in daily_records
        )

        daily_load_ratios = [
            day["passengers"] / self.bus_capacity
            for day in daily_records
        ]

        max_passengers = max(
            day["passengers"] for day in daily_records
        )

        overloaded_days = [
            index + 1
            for index, day in enumerate(daily_records)
            if day["passengers"]
            > self.bus_capacity * self.overload_threshold
        ]

        capacity_exceeded_days = [
            index + 1
            for index, day in enumerate(daily_records)
            if day["passengers"] > self.bus_capacity
        ]

        average_journey_time = (
            total_journey_time / len(daily_records)
        )

        fuel_per_km = total_fuel / total_distance

        passengers_per_hour = (
            total_passengers / total_journey_time
            if total_journey_time > 0 else 0
        )

        average_load_percent = (
            mean(daily_load_ratios) * 100
        )

        overloaded = bool(overloaded_days)

        # Lower fuel consumption per km and shorter journey time
        # satisfy the configurable operating-efficiency criteria.
        efficient = (
            average_journey_time <= self.max_journey_time
            and fuel_per_km <= self.max_fuel_per_km
            and not overloaded
        )

        return {
            "days_analysed": len(daily_records),
            "total_passengers": total_passengers,
            "total_journey_time": round(total_journey_time, 2),
            "average_journey_time": round(
                average_journey_time, 2
            ),
            "total_fuel": round(total_fuel, 2),
            "total_distance": round(total_distance, 2),
            "fuel_per_km": round(fuel_per_km, 3),
            "passengers_per_hour": round(
                passengers_per_hour, 2
            ),
            "average_load_percent": round(
                average_load_percent, 2
            ),
            "max_passengers": max_passengers,
            "capacity_exceeded_days": capacity_exceeded_days,
            "overloaded_days": overloaded_days,
            "overloaded": overloaded,
            "efficient": efficient
        }

    def analyse_all_routes(self, route_data):
        self.validate_data(route_data)

        results = {
            route: self.analyse_route(records)
            for route, records in route_data.items()
        }

        # Rank by fuel efficiency, journey time, and passenger throughput.
        ranking = sorted(
            results.items(),
            key=lambda item: (
                item[1]["overloaded"],
                item[1]["fuel_per_km"],
                item[1]["average_journey_time"],
                -item[1]["passengers_per_hour"]
            )
        )

        return results, ranking

    @staticmethod
    def display_report(results, ranking):
        print("\n========== BUS ROUTE PERFORMANCE REPORT ==========")

        for route, stats in results.items():
            print(f"\nRoute: {route}")
            print("Days Analysed:", stats["days_analysed"])
            print("Total Passengers:", stats["total_passengers"])
            print("Total Journey Time:", stats["total_journey_time"])
            print("Average Journey Time:", stats["average_journey_time"])
            print("Total Fuel Used:", stats["total_fuel"])
            print("Total Distance:", stats["total_distance"])
            print("Fuel per km:", stats["fuel_per_km"])
            print("Passengers per hour:", stats["passengers_per_hour"])
            print("Average Capacity Utilisation:",
                  f'{stats["average_load_percent"]}%')
            print("Maximum Daily Demand:", stats["max_passengers"])
            print("Capacity Exceeded Days:",
                  stats["capacity_exceeded_days"])
            print("Overloaded Days:", stats["overloaded_days"])
            print("Overloaded Route:",
                  "YES" if stats["overloaded"] else "NO")
            print("Operating Efficiently:",
                  "YES" if stats["efficient"] else "NO")

        print("\n========== OPERATING EFFICIENCY RANKING ==========")

        for rank, (route, stats) in enumerate(ranking, start=1):
            print(
                f"{rank}. {route} | "
                f"Fuel/km: {stats['fuel_per_km']} | "
                f"Avg journey time: "
                f"{stats['average_journey_time']} | "
                f"Passengers/hour: {stats['passengers_per_hour']}"
            )

        print("==================================================")


def main():
    try:
        capacity = int(input("Enter bus capacity: "))
        days = int(input("Enter number of days to analyse: "))

        if days <= 0:
            raise ValueError("Number of days must be positive.")

        route_count = int(input("Enter number of routes: "))

        if route_count <= 0:
            raise ValueError("Number of routes must be positive.")

        route_data = {}

        for route_index in range(route_count):
            route_name = input(
                f"\nEnter name of route {route_index + 1}: "
            ).strip()

            if not route_name or route_name in route_data:
                raise ValueError(
                    "Route names must be non-empty and unique."
                )

            route_data[route_name] = []

            for day in range(1, days + 1):
                print(f"\n{route_name} - Day {day}")

                passengers = int(
                    input("Passengers: ")
                )
                journey_time = float(
                    input("Journey time in hours: ")
                )
                fuel_used = float(
                    input("Fuel used in litres: ")
                )
                distance = float(
                    input("Distance travelled in km: ")
                )

                route_data[route_name].append({
                    "passengers": passengers,
                    "journey_time": journey_time,
                    "fuel_used": fuel_used,
                    "distance": distance
                })

        max_time = float(
            input("\nMaximum acceptable average journey time (hours): ")
        )
        max_fuel_per_km = float(
            input("Maximum acceptable fuel usage (litres/km): ")
        )
        overload_threshold = float(
            input("Overload threshold (e.g. 1.0 for 100% capacity): ")
        )

        system = BusRoutePerformanceAnalysis(
            bus_capacity=capacity,
            max_journey_time=max_time,
            max_fuel_per_km=max_fuel_per_km,
            overload_threshold=overload_threshold
        )

        results, ranking = system.analyse_all_routes(route_data)
        system.display_report(results, ranking)

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()
