from flask import Blueprint, jsonify
from flask_pydantic import validate

from app.modules.items import service
from app.modules.items.schemas import CreateItemSchema, UpdateItemSchema

items_bp = Blueprint("items", __name__, url_prefix="/api/items")


@items_bp.errorhandler(service.ItemNotFoundError)
def handle_not_found(err):
    return jsonify({"error": str(err)}), 404


@items_bp.post("/")
@validate()
def create_item(body: CreateItemSchema):
    """Create a new item.
    ---
    tags:
      - Items
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [name, price]
            properties:
              name:
                type: string
                minLength: 1
                maxLength: 255
                example: Laptop
              price:
                type: number
                minimum: 0
                example: 999.99
              description:
                type: string
                maxLength: 1000
              in_stock:
                type: boolean
                default: true
    responses:
      201:
        description: Item created
      400:
        description: Validation error
    """
    item = service.create_item(body)
    return jsonify(item.to_dict()), 201


@items_bp.get("/")
def list_items():
    """List all items.
    ---
    tags:
      - Items
    responses:
      200:
        description: List of all non-deleted items
    """
    items = service.get_all_items()
    return jsonify([i.to_dict() for i in items])


@items_bp.get("/<int:item_id>")
def get_item(item_id: int):
    """Get a single item by ID.
    ---
    tags:
      - Items
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
    responses:
      200:
        description: Item found
      404:
        description: Item not found
    """
    return jsonify(service.get_item(item_id).to_dict())


@items_bp.patch("/<int:item_id>")
@validate()
def update_item(item_id: int, body: UpdateItemSchema):
    """Partially update an item (PATCH semantics).
    ---
    tags:
      - Items
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                minLength: 1
                maxLength: 255
              price:
                type: number
                minimum: 0
              description:
                type: string
                maxLength: 1000
              in_stock:
                type: boolean
    responses:
      200:
        description: Item updated
      404:
        description: Item not found
    """
    return jsonify(service.update_item(item_id, body).to_dict())


@items_bp.delete("/<int:item_id>")
def delete_item(item_id: int):
    """Soft-delete an item.
    ---
    tags:
      - Items
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
    responses:
      204:
        description: Item soft-deleted
      404:
        description: Item not found
    """
    service.delete_item(item_id)
    return "", 204
