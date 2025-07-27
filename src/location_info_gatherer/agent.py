"""
Session Timeline Traffic & Weather Agent

This agent reads user timeline locations from previous session info,
fetches traffic updates between consecutive locations using Google Maps Directions API,
and gets weather updates for each location using OpenWeather API.
Outputs a JSON array with traffic and weather summaries.
"""

from google.adk.agents import LlmAgent
import requests
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

GEMINI_MODEL = "gemini-2.0-flash"

def get_directions_and_traffic_summary(origin: str, destination: str, api_key: str) -> Dict[str, str]:
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin}&destination={destination}&departure_time=now&key={api_key}"
    )
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "OK":
        return {
            "title": f"Unable to retrieve directions: {origin.replace('+', ' ')} → {destination.replace('+', ' ')}",
            "description": data.get("error_message", "Could not fetch directions.")
        }

    route = data["routes"][0]
    leg = route["legs"][0]
    duration = leg.get("duration", {}).get("text", "N/A")
    duration_in_traffic = leg.get("duration_in_traffic", {}).get("text", duration)
    distance = leg.get("distance", {}).get("text", "N/A")

    # Analyze traffic
    if duration_in_traffic != duration:
        traffic_status = "Heavy traffic"
        try:
            normal = int(duration.split()[0])
            traffic = int(duration_in_traffic.split()[0])
            if traffic <= normal + 5:
                traffic_status = "Light traffic"
            elif traffic <= normal + 15:
                traffic_status = "Moderate traffic"
        except Exception:
            pass
    else:
        traffic_status = "Light traffic"

    title = f"{traffic_status} from {origin.replace('+', ' ')} to {destination.replace('+', ' ')}"
    description = (
        f"Distance: {distance}. Estimated time: {duration_in_traffic} (normal: {duration}). "
        f"Traffic status: {traffic_status}."
    )

    return {
        "title": title,
        "description": description
    }

def get_weather_summary(location: str, api_key: str) -> Dict[str, str]:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get("cod") != 200:
        return {
            "title": f"Weather unavailable for {location.replace('+', ' ')}",
            "description": data.get("message", "Could not fetch weather.")
        }
    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    city = data["name"]
    title = f"Weather in {city}"
    description = f"{weather}. Temperature: {temp}°C."
    return {
        "title": title,
        "description": description
    }

def get_session_timeline_locations(session_info: Dict[str, Any]) -> List[str]:
    """
    Extracts ordered list of location strings from previous session info.
    Assumes session_info  c  vc ggfcdvc ontains a 'timeline' key with list of location names.
    """
    # For testing, return dummy timeline data if not present
    return session_info.get("timeline",[
  {
    "day": "Monday",
    "date": "2025-07-28",
    "activities": [
      {
        "time_start": "07:00",
        "time_end": "07:30",
        "activity": "Wake up, morning routine",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "07:30",
        "time_end": "08:15",
        "activity": "Breakfast and preparing for office",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "08:15",
        "time_end": "09:15",
        "activity": "Commute to Office",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "Office Cab/Bike"
      },
      {
        "time_start": "09:15",
        "time_end": "13:00",
        "activity": "Work: Stand-up, coding, code reviews",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "13:00",
        "time_end": "14:00",
        "activity": "Lunch at Office Cafeteria",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "14:00",
        "time_end": "18:30",
        "activity": "Work: Meetings, debugging, feature development",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "18:30",
        "time_end": "19:30",
        "activity": "Commute back home",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Office Cab/Bike"
      },
      {
        "time_start": "19:30",
        "time_end": "20:30",
        "activity": "Dinner and unwinding",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "20:30",
        "time_end": "22:00",
        "activity": "Personal project / Upskilling (e.g., LeetCode)",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "22:00",
        "time_end": "23:00",
        "activity": "Relaxing, social media, light reading",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "23:00",
        "time_end": "07:00 (next day)",
        "activity": "Sleep",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      }
    ]
  },
  {
    "day": "Tuesday",
    "date": "2025-07-29",
    "activities": [
      {
        "time_start": "07:00",
        "time_end": "08:00",
        "activity": "Wake up, morning workout",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "08:00",
        "time_end": "09:00",
        "activity": "Breakfast, preparing for WFH",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "09:00",
        "time_end": "13:00",
        "activity": "Work from Home: Development, team syncs",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "13:00",
        "time_end": "14:00",
        "activity": "Lunch break, cooking at home",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "14:00",
        "time_end": "18:00",
        "activity": "Work from Home: Collaboration, documentation",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "18:00",
        "time_end": "19:00",
        "activity": "Evening walk / Groceries",
        "location": "Local Market (Marathahalli)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "19:00",
        "time_end": "20:00",
        "activity": "Dinner prep and dinner",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "20:00",
        "time_end": "22:30",
        "activity": "Reading tech blogs, online courses",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "22:30",
        "time_end": "23:30",
        "activity": "Entertainment (streaming)",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "23:30",
        "time_end": "07:00 (next day)",
        "activity": "Sleep",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      }
    ]
  },
  {
    "day": "Wednesday",
    "date": "2025-07-30",
    "activities": [
      {
        "time_start": "07:00",
        "time_end": "07:30",
        "activity": "Wake up, morning routine",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "07:30",
        "time_end": "08:15",
        "activity": "Breakfast and preparing for office",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "08:15",
        "time_end": "09:15",
        "activity": "Commute to Office (peak traffic day)",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "Office Cab/Metro + Auto"
      },
      {
        "time_start": "09:15",
        "time_end": "13:00",
        "activity": "Work: Client meetings, project planning",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "13:00",
        "time_end": "14:00",
        "activity": "Lunch at a nearby restaurant with colleagues (e.g., The Biere Club or a local eatery)",
        "location": "Bellandur/Sarjapur Road area",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "14:00",
        "time_end": "18:00",
        "activity": "Work: Team collaboration, problem-solving",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "18:00",
        "time_end": "19:00",
        "activity": "Networking event/Meetup (e.g., Bangalore Software Engineers Meetup)",
        "location": "Near office/Koramangala",
        "mode_of_transport": "Office Cab/Auto"
      },
      {
        "time_start": "19:00",
        "time_end": "20:30",
        "activity": "Commute back home",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Office Cab/Metro + Auto"
      },
      {
        "time_start": "20:30",
        "time_end": "21:30",
        "activity": "Dinner",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "21:30",
        "time_end": "23:00",
        "activity": "Casual Browse/ unwinding",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "23:00",
        "time_end": "07:00 (next day)",
        "activity": "Sleep",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      }
    ]
  },
  {
    "day": "Thursday",
    "date": "2025-07-31",
    "activities": [
      {
        "time_start": "07:30",
        "time_end": "08:00",
        "activity": "Wake up, gentle stretches",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "08:00",
        "time_end": "09:00",
        "activity": "Breakfast and news",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "09:00",
        "time_end": "13:30",
        "activity": "Work from Home: Deep work, coding",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "13:30",
        "time_end": "14:30",
        "activity": "Lunch delivery / quick meal",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "14:30",
        "time_end": "19:00",
        "activity": "Work from Home: Code push, testing, mentorship",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "19:00",
        "time_end": "20:00",
        "activity": "Visit a friend / coffee shop (e.g., Third Wave Coffee Roasters)",
        "location": "Nearby cafe",
        "mode_of_transport": "Bike/Auto"
      },
      {
        "time_start": "20:00",
        "time_end": "21:00",
        "activity": "Dinner",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "21:00",
        "time_end": "23:00",
        "activity": "Gaming / Hobbies",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "23:00",
        "time_end": "07:30 (next day)",
        "activity": "Sleep",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      }
    ]
  },
  {
    "day": "Friday",
    "date": "2025-08-01",
    "activities": [
      {
        "time_start": "07:00",
        "time_end": "07:30",
        "activity": "Wake up, morning routine",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "07:30",
        "time_end": "08:15",
        "activity": "Breakfast and preparing for office",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "08:15",
        "time_end": "09:15",
        "activity": "Commute to Office",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "Office Cab/Bike"
      },
      {
        "time_start": "09:15",
        "time_end": "13:00",
        "activity": "Work: Sprint review, planning for next week",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "13:00",
        "time_end": "14:00",
        "activity": "Team lunch out (e.g., Social, Doolally Taproom)",
        "location": "Koramangala/Indiranagar",
        "mode_of_transport": "Office Cab/Auto"
      },
      {
        "time_start": "14:00",
        "time_end": "17:30",
        "activity": "Work: Final tasks, clearing backlog",
        "location": "Office (Outer Ring Road, Bellandur)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "17:30",
        "time_end": "18:30",
        "activity": "Commute back home",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Office Cab/Bike"
      },
      {
        "time_start": "18:30",
        "time_end": "20:00",
        "activity": "Relax, prepare for weekend",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "20:00",
        "time_end": "23:00",
        "activity": "Dinner out with friends / Home party",
        "location": "Indiranagar / Koramangala restaurant/pub",
        "mode_of_transport": "Cab/Auto"
      },
      {
        "time_start": "23:00",
        "time_end": "00:00",
        "activity": "Travel back home",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Cab"
      },
      {
        "time_start": "00:00",
        "time_end": "08:00 (next day)",
        "activity": "Sleep",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      }
    ]
  },
  {
    "day": "Saturday",
    "date": "2025-08-02",
    "activities": [
      {
        "time_start": "08:00",
        "time_end": "09:00",
        "activity": "Wake up, leisurely morning",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "09:00",
        "time_end": "10:00",
        "activity": "Breakfast at a local eatery",
        "location": "Marathahalli",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "10:00",
        "time_end": "14:00",
        "activity": "Outdoor activity: Trekking to Nandi Hills or visiting Bannerghatta National Park",
        "location": "Nandi Hills / Bannerghatta National Park",
        "mode_of_transport": "Car (self-drive/carpool)"
      },
      {
        "time_start": "14:00",
        "time_end": "15:00",
        "activity": "Lunch near activity spot",
        "location": "Near Nandi Hills / Bannerghatta",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "15:00",
        "time_end": "17:00",
        "activity": "Travel back to Bangalore",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Car (self-drive/carpool)"
      },
      {
        "time_start": "17:00",
        "time_end": "19:00",
        "activity": "Relaxing, catching up on chores",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "19:00",
        "time_end": "22:00",
        "activity": "Movie night at home or cinema (e.g., PVR Forum Mall)",
        "location": "Home / Forum Mall (Koramanagala)",
        "mode_of_transport": "Cab/Auto"
      },
      {
        "time_start": "22:00",
        "time_end": "23:00",
        "activity": "Dinner",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "23:00",
        "time_end": "08:30 (next day)",
        "activity": "Sleep",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      }
    ]
  },
  {
    "day": "Sunday",
    "date": "2025-08-03",
    "activities": [
      {
        "time_start": "08:30",
        "time_end": "09:30",
        "activity": "Leisurely wake up, coffee",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "09:30",
        "time_end": "11:00",
        "activity": "Brunch at a cafe (e.g., Sly Granny, Matteo Coffee)",
        "location": "Indiranagar/Koramangala cafe",
        "mode_of_transport": "Bike/Auto"
      },
      {
        "time_start": "11:00",
        "time_end": "14:00",
        "activity": "Errands, grocery shopping, household tasks",
        "location": "Local Market / Supermarket",
        "mode_of_transport": "Bike/Auto"
      },
      {
        "time_start": "14:00",
        "time_end": "15:00",
        "activity": "Lunch at home",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "15:00",
        "time_end": "18:00",
        "activity": "Relaxing, reading, planning for the week ahead",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "18:00",
        "time_end": "19:30",
        "activity": "Evening walk / Light exercise",
        "location": "Nearby park",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "19:30",
        "time_end": "20:30",
        "activity": "Dinner",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "Foot"
      },
      {
        "time_start": "20:30",
        "time_end": "22:00",
        "activity": "Watching a series / unwinding",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      },
      {
        "time_start": "22:00",
        "time_end": "07:00 (next day)",
        "activity": "Sleep, preparing for the work week",
        "location": "Home (Marathahalli, Bangalore)",
        "mode_of_transport": "N/A"
      }
    ]
  }
])

def get_traffic_and_weather_updates(
    session_info: Dict[str, Any],
    google_maps_api_key: str,
    openweather_api_key: str
) -> List[Dict[str, str]]:
    """
    For each consecutive pair of locations in the session timeline,
    fetch traffic updates, and for each location, fetch weather updates.
    Returns a list of dicts with 'title' and 'description'.
    """
    locations = get_session_timeline_locations(session_info)
    results = []

    # Traffic updates between consecutive locations
    for i in range(len(locations) - 1):
        origin = locations[i]
        destination = locations[i + 1]
        traffic = get_directions_and_traffic_summary(origin, destination, google_maps_api_key)
        results.append(traffic)

    # Weather updates for each location
    for loc in locations:
        weather = get_weather_summary(loc, openweather_api_key)
        results.append(weather)

    return results

root_agent = LlmAgent(
    name="session_timeline_traffic_weather_agent",
    model=GEMINI_MODEL,
    instruction="""
You are a Session Timeline Traffic & Weather Agent.

Given a user's previous session info containing a timeline of locations:
1. For each consecutive pair, fetch recent traffic info using Google Maps Directions API.
2. For each location, fetch current weather using OpenWeather API.
3. Output a JSON array, each object with:
   - title: Short summary of traffic or weather.
   - description: Brief details about the route or weather.
""",
    description="Fetches traffic and weather updates for session timeline locations.",
    tools=[get_traffic_and_weather_updates],
    output_key="timeline_updates",
)

# Example usage:
session_info = {
    "timeline": [
        "Times+Square,New+York,NY",
        "Central+Park,New+York,NY",
        "Empire+State+Building,New+York,NY"
    ]
}
def run_agent_for_session_updates(session_info: dict) -> list:
  load_dotenv()
  google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
  openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
  if not google_maps_api_key or not openweather_api_key:
    raise RuntimeError("API keys not found in environment variables.")
  return get_traffic_and_weather_updates(session_info, google_maps_api_key, openweather_api_key)

# Example usage:
if __name__ == "__main__":
  updates = run_agent_for_session_updates(session_info)
  print(updates)
