from scheduling.serializers import RouteSerializer
def test_route_requires_two_stops(): assert not RouteSerializer(data={"name":"Short","stops":["A"],"estimated_duration_minutes":2}).is_valid()
def test_route_accepts_ordered_stop_names(): assert RouteSerializer(data={"name":"Line","stops":["A","B"],"estimated_duration_minutes":2}).is_valid()

