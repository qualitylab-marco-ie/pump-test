import time
import logging

from utils import misc, file_utils as file_utils, debug_utils as debug_utils

from gpiozero import OutputDevice
from pump.carb import monitor_flow_rate

RELAY_1_PIN = 27
RELAY_2_PIN = 22

relay1 = OutputDevice(RELAY_1_PIN, active_high=False)  # active_low relays
relay2 = OutputDevice(RELAY_2_PIN, active_high=False)  # active_low relays

def relay_toggle(relay: OutputDevice) -> None:
    relay.toggle()


def main() -> None:
    aq_pump = "AQUATEC_PUMP"
    aq_pump_ppl = config["PROD"]["AQUATEC_PUMP"]

    ca_pump = "CHARLES_AUSTEN_PUMP"
    ca_pump_ppl = config["PROD"]["CHARLES_AUSTEN_PUMP"]
    try:
        if file_utils.run_file_checks():
            while True:
                relay1.on()
                
                ca_pump_data = monitor_flow_rate(pulses_per_liter=ca_pump_ppl, pump=ca_pump, duration=config["PROD"]["PUMP_ON_TIME"])
                
                debug_utils.debug_message(ca_pump_data, logging.INFO)
                print("")
                file_utils.append_to_file(ca_pump_data)
                
                relay1.off()
                time.sleep(10) # 10 Seconds for next pump cycle
                relay2.on()

                aq_pump_data = monitor_flow_rate(pulses_per_liter=aq_pump_ppl, pump=aq_pump, duration=config["PROD"]["PUMP_ON_TIME"])
                debug_utils.debug_message(aq_pump_data, logging.INFO)
                print("")
                file_utils.append_to_file(aq_pump_data)

                relay2.off()
                
                time.sleep(10) #10 Seconds for next full cycle
    except Exception as e:
        debug_utils.debug_message(e, logging.ERROR)
    finally:
        relay1.off()
        relay2.off()


if __name__ == "__main__":
    config = misc.read_config_file()
    

    main()