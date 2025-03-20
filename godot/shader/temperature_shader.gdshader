shader_type spatial;

uniform vec4 sensors[100];
uniform int sensor_count;
varying vec3 world_pos;

void vertex() {
	// Convert local position to world position
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	float numerator = 0.0;
	float denominator = 0.0;
	for (int i = 0; i < sensor_count; i++) {
		float dist = distance(world_pos, vec3(sensors[i].x, sensors[i].y, sensors[i].z));
		if (dist != 0.0) {
			float invDist = 1.0 / dist;
			numerator += sensors[i].w * invDist;
			denominator += invDist;
		}
	}
	float temperature = (numerator/denominator)/100.0;
	ALBEDO = vec3(temperature*temperature, 0.1, 1.0 - temperature*temperature);
	ALPHA = 1.0 - temperature * temperature;
	EMISSION = ALBEDO.rgb / 2.0;
}


void light() {
	// Called for every pixel for every light affecting the material.
	// Uncomment to replace the default light processing function with this one.
}
