class FavoriteAlreadyExistsError(Exception):
    # дубль пары user+listing — вернём 409
    def __init__(self, user_id: int, listing_id: int):
        self.user_id = user_id
        self.listing_id = listing_id
        super().__init__(f"Favorite already exists: user_id={user_id}, listing_id={listing_id}")


class ListingNotFoundError(Exception):
    # listing_id не найден — вернём 404
    def __init__(self, listing_id: int):
        self.listing_id = listing_id
        super().__init__(f"Listing not found: id={listing_id}")
