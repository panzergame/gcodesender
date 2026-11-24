import json


class ParsingGCodeFileException(Exception):
    pass


class GCodeInspector:
    def __init__(self, filename):
        self.filename = filename

        self._metadata = self._extract_metadata()

    def _parse_metadata_json(self, text: str):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    def _extract_metadata(self):
        with open(self.filename) as file:
            comments = filter(lambda line: line.startswith(';'), file)

            def iterate_metadata():
                it = iter(comments)
                while not (line := next(it)).startswith('; metadata_json ='):
                    pass

                for line in it:
                    yield line[2:]

            json_text = ''.join(iterate_metadata())
            return self._parse_metadata_json(json_text)

    @property
    def bounding_rect_gcodes(self) -> [str]:
        return None if self._metadata is None else self._metadata['bounding_rect_gcodes']
