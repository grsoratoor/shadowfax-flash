"""
Basic usage example for the Shadowfax Flash API client.
"""
import asyncio
import os
from dotenv import load_dotenv

from shadowfax_flash import ShadowfaxFlashClient, Environment
from shadowfax_flash.models import (
    LocationDetails,
    DropLocationDetails,
    OrderDetails,
    UserDetails,
    Validations,
    Communications
)

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.getenv("SHADOWFAX_API_KEY")
CREDITS_KEY = os.getenv("SHADOWFAX_CREDITS_KEY")
STORE_BRAND_ID = os.getenv("SHADOWFAX_STORE_BRAND_ID")

async def main():
    if not all([API_KEY, CREDITS_KEY, STORE_BRAND_ID]):
        print("Error: Please set SHADOWFAX_API_KEY, SHADOWFAX_CREDITS_KEY, and SHADOWFAX_STORE_BRAND_ID environment variables")
        return

    # Initialize the client
    async with ShadowfaxFlashClient(
        api_key=API_KEY,
        environment=Environment.STAGING  # Use PRODUCTION for live environment
    ) as client:
        # Example 1: Validate credits key
        print("Validating credits key...")
        try:
            validation = await client.validate_credits_key(
                credits_key=CREDITS_KEY,
                store_brand_id=STORE_BRAND_ID
            )
            print(f"Credits validation: {validation}")
        except Exception as e:
            print(f"Error validating credits: {e}")
            return

        # Example 2: Check serviceability
        print("\nChecking serviceability...")
        try:
            serviceability = await client.check_serviceability(
                pickup_details={
                    "address": "Koramangala, Bangalore, Karnataka 560034",
                    "latitude": 12.9352,
                    "longitude": 77.6245
                },
                drop_details={
                    "address": "HSR Layout, Bangalore, Karnataka 560102",
                    "latitude": 12.9113,
                    "longitude": 77.6475
                }
            )
            print(f"Serviceability check: {serviceability}")
        except Exception as e:
            print(f"Error checking serviceability: {e}")

        # Example 3: Create an order
        print("\nCreating an order...")
        try:
            order_response = await client.create_order(
                pickup_details=LocationDetails(
                    name="John's Store",
                    contact_number="9876543210",
                    address="123, 1st Cross, Koramangala, Bangalore - 560034",
                    landmark="Near Forum Mall",
                    latitude=12.9352,
                    longitude=77.6245
                ),
                drop_details=DropLocationDetails(
                    name="Jane Smith",
                    contact_number="9876543211",
                    address="456, 27th Main, HSR Layout, Bangalore - 560102",
                    landmark="Near BDA Complex",
                    latitude=12.9113,
                    longitude=77.6475
                ),
                order_details=OrderDetails(
                    order_id=f"ORDER{os.urandom(4).hex().upper()}",
                    is_prepaid=False,
                    cash_to_be_collected=150.0,
                    delivery_charge_to_be_collected_from_customer=True
                ),
                user_details=UserDetails(
                    contact_number="9876543210",
                    credits_key=CREDITS_KEY
                ),
                validations=Validations(
                    pickup={"is_otp_required": False},
                    drop={"is_otp_required": True}
                ),
                communications=Communications(
                    send_sms_to_pickup_person=True,
                    send_sms_to_drop_person=True
                )
            )
            
            print(f"Order created successfully!")
            print(f"Order ID: {order_response.get('flash_order_id')}")
            print(f"Pickup OTP: {order_response.get('pickup_otp')}")
            print(f"Drop OTP: {order_response.get('drop_otp')}")
            
            # Example 4: Track the order
            if order_response.get("flash_order_id"):
                print("\nTracking order status...")
                try:
                    tracking = await client.track_order(
                        order_id=order_response["flash_order_id"]
                    )
                    print(f"Order status: {tracking.status}")
                    if tracking.rider_name:
                        print(f"Rider: {tracking.rider_name} ({tracking.rider_contact_number})")
                except Exception as e:
                    print(f"Error tracking order: {e}")
            
        except Exception as e:
            print(f"Error creating order: {e}")

if __name__ == "__main__":
    asyncio.run(main())
