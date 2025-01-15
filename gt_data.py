import struct 
from datetime import timedelta
import json

class GT_Data():
    def __init__(self, data):
        self.best_lap_time = struct.unpack('i', data[0x78:0x78 + 4])[0]
        self.last_lap_time = struct.unpack('i', data[0x7C:0x7C + 4])[0]
        self.current_lap_number = struct.unpack('h', data[0x74:0x74 + 2])[0]
        self.current_gear = struct.unpack('B', data[0x90:0x90 + 1])[0] & 0b00001111
        self.car_speed = 3.6 * struct.unpack('f', data[0x4C:0x4C + 4])[0]
        self.time_on_track = timedelta(
            seconds=round(struct.unpack('i', data[0x80:0x80 + 4])[0] / 1000))  # time of day on track

        self.total_laps = struct.unpack('h', data[0x76:0x76 + 2])[0]  # total laps

        self.current_position = struct.unpack('h', data[0x84:0x84 + 2])[0]  # current position
        self.total_positions = struct.unpack('h', data[0x86:0x86 + 2])[0]  # total positions

        self.car_id = struct.unpack('i', data[0x124:0x124 + 4])[0]  # car id

        self.throttle_percent = struct.unpack('B', data[0x91:0x91 + 1])[0] / 2.55  # throttle as percent 
        self.rpm = struct.unpack('f', data[0x3C:0x3C + 4])[0]  # rpm``
        self.brake_pressure = struct.unpack('B', data[0x92:0x92 + 1])[0] / 2.55  # brake as percent 

        # self.boost = struct.unpack('f', data[0x50:0x50 + 4])[0] - 1  # boost
        # self.is_paused = bin(struct.unpack('B', data[0x8E:0x8E + 1])[0])[-2] == '1'
        # self.in_race = bin(struct.unpack('B', data[0x8E:0x8E + 1])[0])[-1] == '1'
        
        self.position_x = struct.unpack('f', data[0x04:0x04 + 4])[0]  # pos X
        self.position_y = struct.unpack('f', data[0x08:0x08 + 4])[0]  # pos Y
        self.position_z = struct.unpack('f', data[0x0C:0x0C + 4])[0]  # pos Z

        self.velocity_x = struct.unpack('f', data[0x10:0x10 + 4])[0]  # velocity X m/s 
        self.velocity_y = struct.unpack('f', data[0x14:0x14 + 4])[0]  # velocity Y m/s
        self.velocity_z = struct.unpack('f', data[0x18:0x18 + 4])[0]  # velocity Z m/s
        
        # self.suggested_gear = struct.unpack('B', data[0x90:0x90 + 1])[0] >> 4
        # self.fuel_capacity = struct.unpack('f', data[0x48:0x48 + 4])[0]
        # self.current_fuel = struct.unpack('f', data[0x44:0x44 + 4])[0]  # fuel
        # self.boost = struct.unpack('f', data[0x50:0x50 + 4])[0] - 1

        # self.tyre_diameter_FL = struct.unpack('f', data[0xB4:0xB4 + 4])[0]
        # self.tyre_diameter_FR = struct.unpack('f', data[0xB8:0xB8 + 4])[0]
        # self.tyre_diameter_RL = struct.unpack('f', data[0xBC:0xBC + 4])[0]
        # self.tyre_diameter_RR = struct.unpack('f', data[0xC0:0xC0 + 4])[0]

        # self.type_speed_FL = abs(3.6 * self.tyre_diameter_FL * struct.unpack('f', data[0xA4:0xA4 + 4])[0])
        # self.type_speed_FR = abs(3.6 * self.tyre_diameter_FR * struct.unpack('f', data[0xA8:0xA8 + 4])[0])
        # self.type_speed_RL = abs(3.6 * self.tyre_diameter_RL * struct.unpack('f', data[0xAC:0xAC + 4])[0])
        # self.tyre_speed_RR = abs(3.6 * self.tyre_diameter_RR * struct.unpack('f', data[0xB0:0xB0 + 4])[0])


        # if self.car_speed > 0:
        #     self.tyre_slip_ratio_FL = '{:6.2f}'.format(self.type_speed_FL / self.car_speed)
        #     self.tyre_slip_ratio_FR = '{:6.2f}'.format(self.type_speed_FR / self.car_speed)
        #     self.tyre_slip_ratio_RL = '{:6.2f}'.format(self.type_speed_RL / self.car_speed)
        #     self.tyre_slip_ratio_RR = '{:6.2f}'.format(self.tyre_speed_RR / self.car_speed)

        # self.rpm_rev_warning = struct.unpack('H', data[0x88:0x88 + 2])[0]  # rpm rev warning


        # self.rpm_rev_limiter = struct.unpack('H', data[0x8A:0x8A + 2])[0]  # rpm rev limiter

        # self.estimated_top_speed = struct.unpack('h', data[0x8C:0x8C + 2])[0]  # estimated top speed
        
        # self.clutch = struct.unpack('f', data[0xF4:0xF4 + 4])[0]  # clutch
        # self.clutch_engaged = struct.unpack('f', data[0xF8:0xF8 + 4])[0]  # clutch engaged
        # self.rpm_after_clutch = struct.unpack('f', data[0xFC:0xFC + 4])[0]  # rpm after clutch

        # self.oil_temp = struct.unpack('f', data[0x5C:0x5C + 4])[0]  # oil temp
        # self.water_temp = struct.unpack('f', data[0x58:0x58 + 4])[0]  # water temp

        # self.oil_pressure = struct.unpack('f', data[0x54:0x54 + 4])[0]  # oil pressure
        # self.ride_height = 1000 * struct.unpack('f', data[0x38:0x38 + 4])[0]  # ride height

        # self.tyre_temp_FL = struct.unpack('f', data[0x60:0x60 + 4])[0]  # tyre temp FL
        # self.tyre_temp_FR = struct.unpack('f', data[0x64:0x64 + 4])[0]  # tyre temp FR

        # self.suspension_fl = struct.unpack('f', data[0xC4:0xC4 + 4])[0]  # suspension FL
        # self.suspension_fr = struct.unpack('f', data[0xC8:0xC8 + 4])[0]  # suspension FR

        # self.tyre_temp_rl = struct.unpack('f', data[0x68:0x68 + 4])[0]  # tyre temp RL
        # self.tyre_temp_rr = struct.unpack('f', data[0x6C:0x6C + 4])[0]  # tyre temp RR

        # self.suspension_rl = struct.unpack('f', data[0xCC:0xCC + 4])[0]  # suspension RL
        # self.suspension_rr = struct.unpack('f', data[0xD0:0xD0 + 4])[0]  # suspension RR

        # self.gear_1 = struct.unpack('f', data[0x104:0x104 + 4])[0]  # 1st gear
        # self.gear_2 = struct.unpack('f', data[0x108:0x108 + 4])[0]  # 2nd gear
        # self.gear_3 = struct.unpack('f', data[0x10C:0x10C + 4])[0]  # 3rd gear
        # self.gear_4 = struct.unpack('f', data[0x110:0x110 + 4])[0]  # 4th gear
        # self.gear_5 = struct.unpack('f', data[0x114:0x114 + 4])[0]  # 5th gear
        # self.gear_6 = struct.unpack('f', data[0x118:0x118 + 4])[0]  # 6th gear
        # self.gear_7 = struct.unpack('f', data[0x11C:0x11C + 4])[0]  # 7th gear
        # self.gear_8 = struct.unpack('f', data[0x120:0x120 + 4])[0]  # 8th gear

        # self.struct.unpack('f', data[0x100:0x100+4])[0]					# ??? gear


        # self.rotation_pitch = struct.unpack('f', data[0x1C:0x1C + 4])[0]  # rot Pitch
        # self.rotation_yaw = struct.unpack('f', data[0x20:0x20 + 4])[0]  # rot Yaw
        # self.rotation_roll = struct.unpack('f', data[0x24:0x24 + 4])[0]  # rot Roll

        # self.angular_velocity_x = struct.unpack('f', data[0x2C:0x2C + 4])[0]  # angular velocity X
        # self.angular_velocity_y = struct.unpack('f', data[0x30:0x30 + 4])[0]  # angular velocity Y
        # self.angular_velocity_z = struct.unpack('f', data[0x34:0x34 + 4])[0]  # angular velocity Z

    
    def to_dict(self):
        return self.__dict__
        

  