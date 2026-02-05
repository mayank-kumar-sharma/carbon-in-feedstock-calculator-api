from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Biochar Carbon Credit API")

# -----------------------------
# Constants
# -----------------------------
CO2_CONVERSION = 3.67
EMISSION_DEDUCTION = 0.15

# -----------------------------
# Feedstock Data
# -----------------------------
data = {
    "Rice husk": {"industrial": (0.65, 0.80), "artisanal": (0.55, 0.70)},
    "Wood chips": {"industrial": (0.75, 0.85), "artisanal": (0.60, 0.70)},
    "Corn cobs": {"industrial": (0.65, 0.80), "artisanal": (0.55, 0.65)},
    "Coconut shells": {"industrial": (0.55, 0.70), "artisanal": (0.45, 0.60)},
    "Bamboo": {"industrial": (0.70, 0.82), "artisanal": (0.55, 0.70)},
    "Sugarcane bagasse": {"industrial": (0.60, 0.76), "artisanal": (0.50, 0.65)},
    "Maize stalks": {"industrial": (0.66, 0.77), "artisanal": (0.55, 0.65)},
    "Cotton stalks": {"industrial": (0.65, 0.77), "artisanal": (0.53, 0.65)},
    "Wheat straw": {"industrial": (0.63, 0.75), "artisanal": (0.50, 0.63)},
    "Rice straw": {"industrial": (0.60, 0.74), "artisanal": (0.50, 0.60)},
    "Groundnut shells": {"industrial": (0.67, 0.80), "artisanal": (0.55, 0.67)},
    "Coffee husk": {"industrial": (0.65, 0.77), "artisanal": (0.53, 0.65)},
    "Palm kernel shells": {"industrial": (0.77, 0.86), "artisanal": (0.63, 0.77)},
    "Sewage sludge": {"industrial": (0.52, 0.72), "artisanal": (0.42, 0.58)},
}

# -----------------------------
# Request Model
# -----------------------------
class CalculationInput(BaseModel):
    feedstock: str
    production_type: str
    biochar_mass: float = 1

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "Biochar Carbon Credit API running"}

@app.post("/calculate")
def calculate(input: CalculationInput):

    feedstock = input.feedstock
    production = input.production_type.lower()
    mass = input.biochar_mass

    if feedstock not in data:
        raise HTTPException(status_code=400, detail="Invalid feedstock")

    if production not in ["industrial", "artisanal"]:
        raise HTTPException(status_code=400, detail="production_type must be industrial or artisanal")

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
