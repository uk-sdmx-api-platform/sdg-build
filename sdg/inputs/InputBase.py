class InputBase:
    """Base class for sources of SDG data/metadata."""

    def __init__(self):
        """Constructor for InputBase."""
        self.indicators = {}
        self.fetch()

    def fetch(self):
        """Fetch all data/metadata from source, fetching a list of indicators."""
        raise NotImplementedError
