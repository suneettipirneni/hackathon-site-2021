# -*- coding: utf-8 -*-
"""
    src.api.sponsor
    ~~~~~~~~~~~~~~~

    Functions:

        create_sponsor()

"""
from flask import Blueprint, request
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict
from src.models.sponsor import Sponsor
from src.models.user import ROLES


sponsors_blueprint = Blueprint("sponsors", __name__)


@sponsors_blueprint.route("/sponsors/", methods=["POST"])
def create_sponsor():
    """
    Creates a new Sponsor.
    ---
    tags:
        - sponsor
    summary: Create Sponsor
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Sponsor'
        description: Created Sponsor Object
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        409:
            description: Sorry, that sponsor_name already exists.
        5XX:
            description: Unexpected error.
    """
    data = request.get_json()

    if not data:
        raise BadRequest("Not data")

    try:
        sponsor = Sponsor.createOne(**data, roles=ROLES.SPONSOR)
    except NotUniqueError:
        raise Conflict("Sorry, this sponsor already exists.")
    except ValidationError:
        raise BadRequest("Validation Error")

    """Send Verification Email"""
    token = sponsor.encode_email_token()
    from src.common.mail import send_verification_email
    send_verification_email(sponsor, token)

    res = {
        "status": "success",
        "message": "Sponsor was created!"
    }

    return res, 201


@sponsors_blueprint.route("/sponsors/<sponsorname>", methods=["GET"])
def get_sponsor(sponsorname: str):
    """
    Creates a new Sponsor.
    ---
    tags:
        - sponsor
    summary: Get Sponsor info
    parameters:
        - in: path
          name: sponsorname
          schema:
            type: string
    responses:
        200:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    sponsor_name:
                        type: string
                    events:
                        type: array
                        items:
                            $ref: '#/components/schemas/Event'
                    email:
                        type: string
                    subscription_tier:
                        type: string
                    logo:
                        type: string
        400:
            description: Bad request.
        404:
            description: Sorry, this sponsor doesn't exist.
        5XX:
            description: Unexpected error.
    """
    sponsor = Sponsor.objects(sponsor_name=sponsorname).first()
    if not sponsor:
        raise NotFound("Sorry, this sponsor doesn't exist")

    res = {
        "sponsor_name": sponsor.sponsor_name,
        "email": sponsor.email,
        "subscription_tier": sponsor.subscription_tier,
        "logo": sponsor.logo,
        "events": sponsor.events
    }

    return res, 200
