from route import Route
import config as cfg


class Truck:
    def __init__(self, _id):
        self.id = _id
        self.route = Route()
        self.miles_traveled = 0
        self.max_speed = 18  # Truck can reach a max speed of 18 MPH.
        self.completed_route = False
        self.departure_time = None

    def assign_deliveries(self, deliveries_list):
        self.route.add_deliveries(self.id, deliveries_list)

    def assign_delivery(self, delivery, add_index):
        self.route.add_delivery(self.id, delivery, add_index)

    def will_fit(self, delivery):
        return len(self.get_packages()) + len(delivery.packages) <= 16

    def get_deliveries(self):
        return [delivery for delivery in self.route.deliveries]

    def get_packages(self):
        return [delivery.packages for delivery in self.route.deliveries]

    def start_delivering(self, time):
        self.route.init(time)
        self.departure_time = time
        print(f"Truck {self.id} has started its route at {time}")

    def an_hour_passed(self):
        # If truck has completed its route, return
        if self.completed_route:
            return

        miles_left = self.route.get_miles_left()
        print(f"Truck {self.id} has {miles_left} miles left to go")

        self.miles_traveled += self.max_speed
        self.route.new_miles_driven(18)
        print(f"Truck {self.id} has driven {self.miles_traveled} miles")

        miles_left = self.route.get_miles_left()
        if miles_left is None:
            self.completed_route = True
            print(f"Truck {self.id} has completed route")
            return


def distribute_deliveries_to_trucks(delivery_list):
    for delivery in delivery_list:
        closest_truck = None
        closest_truck_distance = None
        route_add_index = None
        for truck in cfg.trucks:
            if truck.will_fit(delivery):
                (added_distance, add_index) = truck.route.added_distance(delivery)
                if closest_truck is None or added_distance < closest_truck_distance:
                    closest_truck = truck
                    closest_truck_distance = added_distance
                    route_add_index = add_index
        closest_truck.assign_delivery(delivery, route_add_index)


def assign_all_deliveries_to_best_truck(delivery_list):
    closest_truck = None
    closest_truck_distance = None
    route_add_index = None
    for truck in cfg.trucks:
        if truck.will_fit(delivery_list):
            (added_distance, add_index) = truck.route.added_distance(delivery_list)
            if closest_truck is None or added_distance < closest_truck_distance:
                closest_truck = truck
                closest_truck_distance = added_distance
                route_add_index = add_index
    closest_truck.assign_delivery(delivery_list, route_add_index)
