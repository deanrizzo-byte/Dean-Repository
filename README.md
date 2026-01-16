# Rhodesian Ridgeback Breeder Finder

A tool to find top Rhodesian Ridgeback breeders based on AKC awards, health testing, and breed club membership. Browse litter photos and connect with reputable breeders.

## Features

- **Breeder Search & Ranking**: Find breeders ranked by AKC award score
- **Advanced Filters**: Filter by state, minimum champions, Breeder of Merit status, CHIC health testing, RRCUS membership
- **Litter Gallery**: Browse recent litter photos from registered breeders
- **Detailed Profiles**: View breeder awards, health testing records, and available litters
- **REST API**: Programmatic access to breeder data

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ridgeback-breeder-finder.git
cd ridgeback-breeder-finder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the Flask development server
python app.py

# Open http://localhost:5000 in your browser
```

## Project Structure

```
ridgeback-breeder-finder/
├── app.py                    # Flask web application
├── requirements.txt          # Python dependencies
├── ridgeback_finder/         # Core package
│   ├── __init__.py
│   ├── models.py             # Data models (Breeder, Award, Litter, etc.)
│   ├── finder.py             # Search and ranking service
│   └── gallery.py            # Litter image gallery service
├── templates/                # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── search.html
│   ├── breeder.html
│   ├── gallery.html
│   └── breeder_gallery.html
├── static/
│   ├── css/style.css         # Styles
│   ├── js/main.js            # JavaScript
│   └── images/               # Litter photos
└── data/
    └── breeders.json         # Breeder database
```

## AKC Award Scoring

Breeders are ranked by a composite score based on their AKC achievements:

| Award Type | Points |
|------------|--------|
| Grand Champion Platinum (GCHP) | 100 |
| Grand Champion Gold (GCHG) | 80 |
| Grand Champion Silver (GCHS) | 60 |
| Grand Champion Bronze (GCHB) | 50 |
| Grand Champion (GCH) | 40 |
| Champion (CH) | 30 |
| Field Champion (FC) | 50 |
| Master Agility Champion (MACH) | 50 |
| Breeder of Merit Gold | 100 |
| Breeder of Merit | 75 |
| CHIC Health Certified | 50 |
| Master Courser (MC) | 30 |

Bonus points:
- +10 per health test on file
- +25 for RRCUS membership

## API Endpoints

### Get Breeders
```
GET /api/breeders?state=CA&min_champions=2&breeder_of_merit=true
```

### Get Single Breeder
```
GET /api/breeder/{breeder_id}
```

### Get Breeder's Latest Litter Images
```
GET /api/breeder/{breeder_id}/images
```

### Get Recent Gallery Images
```
GET /api/gallery/recent?limit=20
```

### Get Statistics
```
GET /api/stats
```

## Adding Breeders

Edit `data/breeders.json` to add or update breeder information. Each breeder entry supports:

```json
{
  "breeder_id": "unique-id",
  "kennel_name": "Kennel Name",
  "owner_name": "Owner Name",
  "location": "City, ST",
  "state": "ST",
  "website": "https://...",
  "email": "email@example.com",
  "phone": "(555) 555-5555",
  "years_breeding": 10,
  "rrcus_member": true,
  "description": "About the kennel...",
  "akc_awards": [...],
  "health_tests": [...],
  "litters": [...]
}
```

## Health Testing

The tool tracks OFA and genetic health tests important for Rhodesian Ridgebacks:

- **Hip Dysplasia** (OFA or PennHIP)
- **Elbow Dysplasia** (OFA)
- **Thyroid** (OFA)
- **Cardiac** (OFA)
- **Degenerative Myelopathy (DM)** - DNA test
- **Early-Onset Adult Deafness (EOAD)** - DNA test

Breeders with CHIC-certified dogs have completed all recommended tests.

## Future Enhancements

Consider adding:

- **Reviews/Testimonials**: Allow puppy buyers to leave feedback
- **Waiting List Integration**: Track breeder waiting lists
- **Pedigree Database**: Link to dog pedigree information
- **AKC Marketplace Integration**: Pull data from official sources
- **Location-Based Search**: Find breeders near you with map view
- **Price Range Tracking**: Typical puppy pricing by breeder
- **Contract/Guarantee Info**: Health guarantees and return policies
- **Puppy Availability Notifications**: Alert when breeders have litters

## License

MIT License - See LICENSE file for details.

## Disclaimer

Always verify breeder credentials independently and visit in person before purchasing a puppy. This tool aggregates publicly available information but does not guarantee accuracy or endorse any specific breeder.
