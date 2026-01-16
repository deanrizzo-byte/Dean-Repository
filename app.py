"""
Flask web application for Rhodesian Ridgeback Breeder Finder.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pathlib import Path

from ridgeback_finder.finder import BreederFinder
from ridgeback_finder.gallery import LitterGallery, get_image_url

app = Flask(__name__)
CORS(app)

# Initialize finder
finder = BreederFinder()
finder.load_breeders()


@app.route("/")
def index():
    """Home page with top breeders."""
    top_breeders = finder.get_top_breeders(limit=10)
    stats = finder.get_statistics()
    states = finder.get_all_states()
    return render_template(
        "index.html",
        breeders=top_breeders,
        stats=stats,
        states=states
    )


@app.route("/search")
def search():
    """Search breeders with filters."""
    state = request.args.get("state")
    min_champions = int(request.args.get("min_champions", 0))
    require_bom = request.args.get("breeder_of_merit") == "true"
    require_chic = request.args.get("chic") == "true"
    require_rrcus = request.args.get("rrcus") == "true"
    has_puppies = request.args.get("available_puppies") == "true"
    sort_by = request.args.get("sort", "award_score")

    results = finder.search(
        state=state if state else None,
        min_champions=min_champions,
        require_breeder_of_merit=require_bom,
        require_chic=require_chic,
        require_rrcus=require_rrcus,
        has_available_puppies=has_puppies,
        sort_by=sort_by
    )

    states = finder.get_all_states()
    return render_template(
        "search.html",
        breeders=results,
        states=states,
        filters={
            "state": state,
            "min_champions": min_champions,
            "breeder_of_merit": require_bom,
            "chic": require_chic,
            "rrcus": require_rrcus,
            "available_puppies": has_puppies,
            "sort": sort_by
        }
    )


@app.route("/breeder/<breeder_id>")
def breeder_detail(breeder_id: str):
    """Breeder detail page."""
    breeder = finder.get_breeder(breeder_id)
    if not breeder:
        return render_template("404.html"), 404

    gallery = LitterGallery([breeder])
    latest_images = gallery.get_breeder_latest_litter_images(breeder_id)

    return render_template(
        "breeder.html",
        breeder=breeder,
        latest_images=latest_images
    )


@app.route("/gallery")
def gallery():
    """Image gallery page."""
    gallery_service = LitterGallery(finder.breeders)
    recent_images = gallery_service.get_recent_images(limit=50)
    recent_litters = gallery_service.get_recent_litters(limit=10)

    return render_template(
        "gallery.html",
        images=recent_images,
        recent_litters=recent_litters
    )


@app.route("/gallery/breeder/<breeder_id>")
def breeder_gallery(breeder_id: str):
    """Gallery for a specific breeder."""
    breeder = finder.get_breeder(breeder_id)
    if not breeder:
        return render_template("404.html"), 404

    gallery_service = LitterGallery([breeder])
    images = gallery_service.get_all_images()

    return render_template(
        "breeder_gallery.html",
        breeder=breeder,
        images=images
    )


# API Endpoints
@app.route("/api/breeders")
def api_breeders():
    """API endpoint for breeder search."""
    state = request.args.get("state")
    min_champions = int(request.args.get("min_champions", 0))
    require_bom = request.args.get("breeder_of_merit") == "true"
    require_chic = request.args.get("chic") == "true"
    limit = int(request.args.get("limit", 50))

    results = finder.search(
        state=state if state else None,
        min_champions=min_champions,
        require_breeder_of_merit=require_bom,
        require_chic=require_chic
    )[:limit]

    return jsonify({
        "count": len(results),
        "breeders": [b.to_dict() for b in results]
    })


@app.route("/api/breeder/<breeder_id>")
def api_breeder(breeder_id: str):
    """API endpoint for single breeder."""
    breeder = finder.get_breeder(breeder_id)
    if not breeder:
        return jsonify({"error": "Breeder not found"}), 404
    return jsonify(breeder.to_dict())


@app.route("/api/breeder/<breeder_id>/images")
def api_breeder_images(breeder_id: str):
    """API endpoint for breeder's litter images."""
    breeder = finder.get_breeder(breeder_id)
    if not breeder:
        return jsonify({"error": "Breeder not found"}), 404

    gallery_service = LitterGallery([breeder])
    latest_images = gallery_service.get_breeder_latest_litter_images(breeder_id)

    return jsonify({
        "breeder_id": breeder_id,
        "kennel_name": breeder.kennel_name,
        "image_count": len(latest_images),
        "images": [img.to_dict() for img in latest_images]
    })


@app.route("/api/gallery/recent")
def api_recent_images():
    """API endpoint for recent images."""
    limit = int(request.args.get("limit", 20))
    gallery_service = LitterGallery(finder.breeders)
    images = gallery_service.get_recent_images(limit=limit)

    return jsonify({
        "count": len(images),
        "images": [img.to_dict() for img in images]
    })


@app.route("/api/stats")
def api_stats():
    """API endpoint for database statistics."""
    return jsonify(finder.get_statistics())


# Template context processor
@app.context_processor
def utility_processor():
    return {"get_image_url": get_image_url}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
