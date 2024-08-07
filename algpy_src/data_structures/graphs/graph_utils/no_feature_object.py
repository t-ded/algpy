class NoFeature:

    def __repr__(self) -> str:
        return 'NoFeature'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoFeature)
