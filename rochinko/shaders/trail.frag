#version 330

in vec3 v_color;
in float v_lifetime;

out vec4 f_color;

void main() {
    f_color = vec4(v_color, v_lifetime);
}       