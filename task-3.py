
from dataclasses import dataclass
from typing import List, Optional


# -----------------------------------------
# Vehicle Details
# -----------------------------------------

@dataclass
class Vehicle:
    name: str
    mileage: float          # Kilometers per liter
    fuel_price: float       # Price per liter
    tank_capacity: float    # Fuel tank capacity in liters
    current_fuel: float     # Current fuel in liters


# -----------------------------------------
# Fuel and Route Comparison
# -----------------------------------------

class FuelRouteComparison:

    def __init__(
        self,
        distance: float,
        reserve_fuel: float,
        reserve_percent: float = 0.0
    ):
        if distance <= 0:
            raise ValueError("Distance must be greater than zero.")

        if reserve_fuel < 0:
            raise ValueError("Reserve fuel cannot be negative.")

        if not 0 <= reserve_percent <= 100:
            raise ValueError("Reserve percentage must be between 0 and 100.")

        self.distance = distance
        self.reserve_fuel = reserve_fuel
        self.reserve_percent = reserve_percent

    def validate_vehicle(self, vehicle: Vehicle) -> None:
        if not vehicle.name.strip():
            raise ValueError("Vehicle name cannot be empty.")

        if vehicle.mileage <= 0:
            raise ValueError(
                f"{vehicle.name}: Mileage must be greater than zero."
            )

        if vehicle.fuel_price < 0:
            raise ValueError(
                f"{vehicle.name}: Fuel price cannot be negative."
            )

        if vehicle.tank_capacity <= 0:
            raise ValueError(
                f"{vehicle.name}: Tank capacity must be positive."
            )

        if not 0 <= vehicle.current_fuel <= vehicle.tank_capacity:
            raise ValueError(
                f"{vehicle.name}: Current fuel must be between "
                "zero and tank capacity."
            )

    def calculate(self, vehicle: Vehicle) -> dict:
        self.validate_vehicle(vehicle)

        # Fuel required to travel the specified distance
        trip_fuel = self.distance / vehicle.mileage

        # Reserve is the greater of the fixed and percentage amounts.
        required_reserve = max(
            self.reserve_fuel,
            trip_fuel * self.reserve_percent / 100
        )

        total_required = trip_fuel + required_reserve

        # Check whether the tank can hold the trip fuel and reserve.
        tank_feasible = total_required <= vehicle.tank_capacity

        # Check whether current fuel is sufficient for the trip and reserve.
        fuel_feasible = vehicle.current_fuel >= total_required

        feasible = tank_feasible and fuel_feasible

        # Fuel to purchase, assuming the tank is filled only as needed.
        fuel_to_buy = max(0.0, total_required - vehicle.current_fuel)

        # Cost of fuel needed for the journey, excluding reserve.
        trip_cost = trip_fuel * vehicle.fuel_price

        # Cost to purchase enough fuel to complete the trip and retain reserve.
        refuel_cost = fuel_to_buy * vehicle.fuel_price

        return {
            "vehicle": vehicle.name,
            "trip_fuel": round(trip_fuel, 2),
            "required_reserve": round(required_reserve, 2),
            "total_required": round(total_required, 2),
            "current_fuel": round(vehicle.current_fuel, 2),
            "fuel_to_buy": round(fuel_to_buy, 2),
            "trip_cost": round(trip_cost, 2),
            "refuel_cost": round(refuel_cost, 2),
            "tank_feasible": tank_feasible,
            "fuel_feasible": fuel_feasible,
            "feasible": feasible,
        }

    def compare(self, vehicles: List[Vehicle]) -> dict:
        if not vehicles:
            raise ValueError("At least one vehicle is required.")

        results = [self.calculate(v) for v in vehicles]

        # Compare the actual additional purchase cost required.
        feasible_options = [
            result for result in results if result["feasible"]
        ]

        # A vehicle with insufficient current fuel is still feasible
        # if refueling can bring it to the required amount.
        # Tank capacity must accommodate the trip and reserve.
        refuel_feasible = [
            result for result in results if result["tank_feasible"]
        ]

        best_option: Optional[dict] = None

        if refuel_feasible:
            best_option = min(
                refuel_feasible,
                key=lambda result: result["refuel_cost"]
            )

        return {
            "results": results,
            "lowest_cost_option": best_option,
            "already_fuelled_options": feasible_options,
        }


# -----------------------------------------
# Main Program
# -----------------------------------------

if __name__ == "__main__":

    distance = 300  # Journey distance in kilometers

    reserve_fuel = 5       # Minimum reserve in liters
    reserve_percent = 10   # Or 10% of trip fuel, whichever is greater

    vehicles = [
        Vehicle(
            name="Car A",
            mileage=15,
            fuel_price=105,
            tank_capacity=50,
            current_fuel=10
        ),
        Vehicle(
            name="Car B",
            mileage=20,
            fuel_price=103,
            tank_capacity=40,
            current_fuel=20
        ),
        Vehicle(
            name="Bike C",
            mileage=40,
            fuel_price=105,
            tank_capacity=15,
            current_fuel=5
        ),
        Vehicle(
            name="Car D",
            mileage=12,
            fuel_price=100,
            tank_capacity=60,
            current_fuel=40
        ),
    ]

    try:
        comparison = FuelRouteComparison(
            distance=distance,
            reserve_fuel=reserve_fuel,
            reserve_percent=reserve_percent
        )

        report = comparison.compare(vehicles)

        print("\n===== FUEL AND ROUTE COMPARISON =====")
        print(f"Journey Distance: {distance} km")
        print(f"Minimum Reserve: {reserve_fuel} liters")
        print(f"Reserve Percentage: {reserve_percent}%")

        for result in report["results"]:
            print(f"\nVehicle: {result['vehicle']}")
            print(f"Trip Fuel Required: {result['trip_fuel']} L")
            print(f"Required Reserve: {result['required_reserve']} L")
            print(f"Total Fuel Required: {result['total_required']} L")
            print(f"Current Fuel: {result['current_fuel']} L")
            print(f"Fuel to Buy: {result['fuel_to_buy']} L")
            print(f"Journey Fuel Cost: {result['trip_cost']:.2f}")
            print(f"Additional Refueling Cost: {result['refuel_cost']:.2f}")
            print(f"Tank Capacity Feasible: {result['tank_feasible']}")
            print(f"Can Complete Now: {result['feasible']}")

        best = report["lowest_cost_option"]

        print("\n===== LOWEST-COST FEASIBLE OPTION =====")

        if best:
            print("Vehicle:", best["vehicle"])
            print("Fuel to Buy:", best["fuel_to_buy"], "L")
            print("Additional Cost:", f"{best['refuel_cost']:.2f}")
        else:
            print(
                "No vehicle has sufficient tank capacity "
                "for the journey and required reserve."
            )

        if report["already_fuelled_options"]:
            cheapest_ready = min(
                report["already_fuelled_options"],
                key=lambda result: result["trip_cost"]
            )
            print("\nCheapest Vehicle Ready to Depart:")
            print("Vehicle:", cheapest_ready["vehicle"])
            print("Journey Fuel Cost:", f"{cheapest_ready['trip_cost']:.2f}")

    except ValueError as error:
        print("Input Error:", error)
