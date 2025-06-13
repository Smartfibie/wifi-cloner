import pywifi
from pywifi import const
import time
import json

def scan_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(3)
    results = iface.scan_results()

    networks = []
    for network in results:
        networks.append({
            "ssid": network.ssid,
            "bssid": network.bssid,
            "signal": network.signal,
            "channel": network.freq,
            "auth": network.akm
        })

    with open("networks.json", "w") as f:
        json.dump(networks, f, indent=4)

    print("Scan complete. Networks saved to networks.json.")
    return networks

def display_networks(networks):
    for idx, net in enumerate(networks):
        print(f"{idx+1}. SSID: {net['ssid']} | BSSID: {net['bssid']} | Signal: {net['signal']} dBm")

def connect_to_network(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.key = password
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(5)

    if iface.status() == const.IFACE_CONNECTED:
        print("Successfully connected!")
    else:
        print("Failed to connect.")

if __name__ == "__main__":
    print("Scanning networks...")
    networks = scan_networks()
    display_networks(networks)

    choice = int(input("Select a network to connect to (number): ")) - 1
    ssid = networks[choice]["ssid"]
    password = input(f"Enter password for {ssid}: ")
    connect_to_network(ssid, password)
