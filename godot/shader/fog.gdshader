shader_type fog;

uniform vec4 sensors[100];
uniform int sensor_count;

void fog() {
	float numerator = 0.0;
	float denominator = 0.0;
	for (int i = 0; i < sensor_count; i++) {
		float dist = distance(WORLD_POSITION, vec3(sensors[i].x, sensors[i].y, sensors[i].z));
		if (dist != 0.0) {
			float invDist = 1.0 / dist;
			numerator += sensors[i].w * invDist;
			denominator += invDist;
		}
	}
	float temperature = (numerator/denominator)/100.0;
	ALBEDO = vec3(temperature*temperature, 0.0, 1.0 - temperature*temperature);
	DENSITY = 0.0;
	EMISSION = ALBEDO;

}
