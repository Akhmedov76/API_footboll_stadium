import aiohttp
import asyncio


async def get_coordinates_from_address(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        print(data[0]['lat'], data[0]['lon'])
                        latitude = data[0]['lat']
                        longitude = data[0]['lon']
                        return float(latitude), float(longitude)

                    return None
                return None
        except Exception as e:
            return f"API xatosi: {str(e)}"
