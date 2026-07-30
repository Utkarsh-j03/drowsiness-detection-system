import json
import urllib.request
import urllib.error
import time

# Optional GPS (will work only if gpsd is available)
try:
    import gpsd
    gpsd.connect()
    GPS_AVAILABLE = True
except Exception:
    GPS_AVAILABLE = False


class LocationService:
    def __init__(self, google_api_key=None):
        self.google_api_key = google_api_key
        self.last_update_time = None

    # -------------------- GPS --------------------
    def get_gps_location(self):
        if not GPS_AVAILABLE:
            return None

        try:
            packet = gpsd.get_current()
            if packet.mode >= 2:
                return {
                    "source": "GPS",
                    "lat": packet.lat,
                    "lon": packet.lon,
                    "accuracy": "3-10 meters"
                }
        except Exception:
            return None

        return None

    # -------------------- GOOGLE API --------------------
    def get_google_location(self):
        if not self.google_api_key:
            return None

        try:
            url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={self.google_api_key}"

            data = json.dumps({
                "considerIp": True
            }).encode("utf-8")

            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )

            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read())

            location = result.get("location", {})
            accuracy = result.get("accuracy", "unknown")

            return {
                "source": "Google",
                "lat": location.get("lat"),
                "lon": location.get("lng"),
                "accuracy": f"{accuracy} meters"
            }

        except Exception:
            return None

    # -------------------- IP FALLBACK --------------------
    def get_ip_location(self):
        urls = [
            "https://ipapi.co/json/",
            "http://ip-api.com/json/"
        ]

        for url in urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())

                if "ipapi.co" in url:
                    return {
                        "source": "IP",
                        "city": data.get("city"),
                        "region": data.get("region"),
                        "country": data.get("country_name"),
                        "lat": data.get("latitude"),
                        "lon": data.get("longitude"),
                        "accuracy": "~5-50 km"
                    }
                else:
                    return {
                        "source": "IP",
                        "city": data.get("city"),
                        "region": data.get("regionName"),
                        "country": data.get("country"),
                        "lat": data.get("lat"),
                        "lon": data.get("lon"),
                        "accuracy": "~5-50 km"
                    }

            except Exception:
                continue

        return None

    # -------------------- HYBRID --------------------
    def get_best_location(self):
        # 1. GPS
        loc = self.get_gps_location()
        if loc:
            self.last_update_time = time.strftime("%H:%M:%S")
            return loc

        # 2. Google
        loc = self.get_google_location()
        if loc:
            self.last_update_time = time.strftime("%H:%M:%S")
            return loc

        # 3. IP
        loc = self.get_ip_location()
        if loc:
            self.last_update_time = time.strftime("%H:%M:%S")
            return loc

        return None