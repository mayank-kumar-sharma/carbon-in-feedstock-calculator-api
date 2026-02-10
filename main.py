from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Biochar Carbon Credit API", version="1.0")

CO2_CONVERSION = 3.67
EMISSION_DEDUCTION = 0.15

data = {
    "Rice husk": {"industrial": (0.60, 0.75), "artisanal": (0.50, 0.65)},
    "Wood chips": {"industrial": (0.55, 0.80), "artisanal": (0.55, 0.65)},
    "Corn cobs": {"industrial": (0.71, 0.75), "artisanal": (0.50, 0.60)},
    "Coconut shells": {"industrial": (0.45, 0.65), "artisanal": (0.40, 0.55)},
    "Bamboo": {"industrial": (0.62, 0.78), "artisanal": (0.50, 0.65)},
    "Sugarcane bagasse": {"industrial": (0.58, 0.70), "artisanal": (0.45, 0.60)},
    "Maize stalks": {"industrial": (0.73, 0.72), "artisanal": (0.50, 0.60)},
    "Cotton stalks": {"industrial": (0.49, 0.72), "artisanal": (0.38, 0.60)},
    "Wheat straw": {"industrial": (0.62, 0.70), "artisanal": (0.45, 0.58)},
    "Rice straw": {"industrial": (0.61, 0.70), "artisanal": (0.45, 0.55)},
    "Groundnut shells": {"industrial": (0.62, 0.75), "artisanal": (0.50, 0.62)},
    "Coffee husk": {"industrial": (0.60, 0.72), "artisanal": (0.48, 0.60)},
    "Palm kernel shells": {"industrial": (0.65, 0.82), "artisanal": (0.58, 0.72)},
    "Sewage sludge": {"industrial": (0.42, 0.65), "artisanal": (0.35, 0.50)},
}

class CalculationInput(BaseModel):
    feedstock: str
    production_type: str
    biochar_mass: float = 1

@app.get("/")
def home():
    return {"message": "Biochar Carbon Credit API running"}

@app.post("/calculate")
def calculate(input: CalculationInput):

    feedstock = input.feedstock
    production = input.production_type.strip().lower()
    mass = input.biochar_mass

    if feedstock not in data:
        raise HTTPException(status_code=400, detail="Invalid feedstock")

    if production not in ["industrial", "artisanal"]:
        raise HTTPException(status_code=400, detail="production_type must be industrial or artisanal")

    if mass <= 0:
        raise HTTPException(status_code=400, detail="biochar_mass must be positive")

    c_frac, stable_frac = data[feedstock][production]

    stable_carbon = mass * c_frac * stable_frac
    gross_co2 = stable_carbon * CO2_CONVERSION
    net_credits = gross_co2 * (1 - EMISSION_DEDUCTION)

    return {
        "feedstock": feedstock,
        "production_type": production,
        "biochar_mass": mass,
        "carbon_fraction_used": c_frac,
        "stable_fraction_used": stable_frac,
        "stable_carbon": round(stable_carbon, 3),
        "gross_co2": round(gross_co2, 3),
        "net_credits": round(net_credits, 3)
    }
