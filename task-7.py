
import math


class CampusTransportAllocation:

    def __init__(self, routes, bus_capacity, available_buses=None):
        self.routes = routes
        self.bus_capacity = bus_capacity
        self.available_buses = available_buses

        if bus_capacity <= 0:
            raise ValueError("Bus capacity must be greater than zero.")

        if available_buses is not None and available_buses < 0:
            raise ValueError("Available buses cannot be negative.")

        if not routes:
            raise ValueError("At least one route must be provided.")

        for route, passengers in routes.items():
            if not route.strip():
                raise ValueError("Route name cannot be empty.")

            if not isinstance(passengers, int) or isinstance(passengers, bool):
                raise ValueError(
                    f"Passenger demand for {route} must be an integer."
                )

            if passengers < 0:
                raise ValueError(
                    f"Passenger demand for {route} cannot be negative."
                )

    def calculate_allocation(self):
        results = []
        total_buses_needed = 0

        # Calculate the minimum buses required for every route.
        for route, passengers in self.routes.items():
            buses_needed = math.ceil(passengers / self.bus_capacity)
            total_buses_needed += buses_needed

            results.append({
                "route": route,
                "passengers": passengers,
                "buses_needed": buses_needed
            })

        # If the fleet is unlimited, all passengers can be served.
        if self.available_buses is None:
            buses_remaining = total_buses_needed

            for result in results:
                result["buses_allocated"] = result["buses_needed"]
                result["served_passengers"] = result["passengers"]
                result["unserved_passengers"] = 0

        else:
            # Allocate available buses route by route.
            buses_remaining = self.available_buses

            for result in results:
                allocated = min(
                    result["buses_needed"],
                    buses_remaining
                )

                capacity_available = allocated * self.bus_capacity
                served = min(
                    result["passengers"],
                    capacity_available
                )

                result["buses_allocated"] = allocated
                result["served_passengers"] = served
                result["unserved_passengers"] = (
                    result["passengers"] - served
                )

                buses_remaining -= allocated

        total_passengers = sum(self.routes.values())
        total_served = sum(
            result["served_passengers"] for result in results
        )
        total_unserved = total_passengers - total_served
        buses_used = sum(
            result["buses_allocated"] for result in results
        )

        return {
            "routes": results,
            "total_passengers": total_passengers,
            "total_buses_needed": total_buses_needed,
            "available_buses": self.available_buses,
            "buses_used": buses_used,
            "total_served": total_served,
            "total_unserved": total_unserved,
            "unused_buses": (
                max(0, self.available_buses - buses_used)
                if self.available_buses is not None else 0
            )
        }

    @staticmethod
    def display_report(report):
        print("\n===== CAMPUS TRANSPORT ALLOCATION =====")

        print(
            f"{'Route':<15}{'Demand':>10}{'Needed':>10}"
            f"{'Allocated':>12}{'Served':>10}{'Unserved':>11}"
        )
        print("-" * 68)

        for route in report["routes"]:
            print(
                f"{route['route']:<15}"
                f"{route['passengers']:>10}"
                f"{route['buses_needed']:>10}"
                f"{route['buses_allocated']:>12}"
                f"{route['served_passengers']:>10}"
                f"{route['unserved_passengers']:>11}"
            )

        print("-" * 68)
        print("Total passengers:", report["total_passengers"])
        print("Total buses needed:", report["total_buses_needed"])

        if report["available_buses"] is not None:
            print("Available buses:", report["available_buses"])

        print("Buses allocated:", report["buses_used"])
        print("Passengers served:", report["total_served"])
        print("Unserved passengers:", report["total_unserved"])

        if report["available_buses"] is not None:
            print("Unused buses:", report["unused_buses"])

        if report["total_unserved"] == 0:
            print("Status: All passengers can be transported.")
        else:
            print("Status: Additional buses are required.")

        print("=======================================")


def main():
    try:
        bus_capacity = int(input("Enter capacity of each bus: "))
        number_of_routes = int(input("Enter number of routes: "))

        if number_of_routes <= 0:
            raise ValueError("Number of routes must be positive.")

        routes = {}

        for i in range(number_of_routes):
            print(f"\nRoute {i + 1}")
            name = input("Enter route name: ").strip()
            passengers = int(input("Enter passenger demand: "))

            if not name:
                raise ValueError("Route name cannot be empty.")

            if name in routes:
                raise ValueError("Duplicate route names are not allowed.")

            routes[name] = passengers

        fleet_input = input(
            "\nEnter available buses (or press Enter for unlimited): "
        ).strip()

        available_buses = (
            int(fleet_input) if fleet_input else None
        )

        allocation = CampusTransportAllocation(
            routes,
            bus_capacity,
            available_buses
        )

        report = allocation.calculate_allocation()
        allocation.display_report(report)

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()
