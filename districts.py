"""
Bangladesh flood-prone districts with coordinates for Open-Meteo Flood API queries.

Coordinates are approximate district-center points. The Flood API resolves to the
nearest ~5 km GloFAS river grid cell, so exact precision isn't critical. Districts
below were chosen for known historical flood exposure along the Jamuna/Brahmaputra,
Padma, and Surma river systems. Extend this list with more districts as needed.
"""

DISTRICTS = [
    {"name": "Dhaka", "division": "Dhaka", "latitude": 23.8103, "longitude": 90.4125},
    {"name": "Sirajganj", "division": "Rajshahi", "latitude": 24.4534, "longitude": 89.7010},
    {"name": "Bogura", "division": "Rajshahi", "latitude": 24.8465, "longitude": 89.3773},
    {"name": "Kurigram", "division": "Rangpur", "latitude": 25.8054, "longitude": 89.6362},
    {"name": "Gaibandha", "division": "Rangpur", "latitude": 25.3288, "longitude": 89.5281},
    {"name": "Rangpur", "division": "Rangpur", "latitude": 25.7439, "longitude": 89.2752},
    {"name": "Jamalpur", "division": "Mymensingh", "latitude": 24.9375, "longitude": 89.9370},
    {"name": "Faridpur", "division": "Dhaka", "latitude": 23.6070, "longitude": 89.8429},
    {"name": "Sylhet", "division": "Sylhet", "latitude": 24.8949, "longitude": 91.8687},
    {"name": "Chattogram", "division": "Chattogram", "latitude": 22.3569, "longitude": 91.7832},
]
