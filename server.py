import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("DoctorFinder")

@mcp.tool()
def search_top_doctors(city: str, speciality: str, limit: int = 3):
    """
    Finds the top N doctors in a city based on speciality.
    Results are sorted by fee (lowest first) to provide the 'best' recommendations.
    """
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    
    # Using ORDER BY fee ASC and LIMIT to get the top 3
    query = """
        SELECT name, designation, speciality, location, fee 
        FROM doctors 
        WHERE location LIKE ? AND speciality LIKE ?
        ORDER BY fee ASC
        LIMIT ?
    """
    
    cursor.execute(query, (f"%{city}%", f"%{speciality}%", limit))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No doctors found matching those criteria."
    
    return [
        {"name": r[0], "designation": r[1], "speciality": r[2], "location": r[3], "fee": r[4]} 
        for r in rows
    ]

if __name__ == "__main__":
    mcp.run()