#version 330

in vec2 in_pos;
in vec2 in_vel;
in vec3 in_color;
in float in_fade_rate;

out vec3 v_color;
out float v_lifetime;

uniform float time;

void main() {
    vec2 pos = in_pos + in_vel * time;
    gl_Position = vec4(pos, 0.0, 1.0);

    v_color = in_color;
    v_lifetime = 1.0 - (time * in_fade_rate);
}