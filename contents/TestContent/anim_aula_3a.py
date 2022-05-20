from uaibot import *
import numpy as np

width=800
height=600

robot = Robot.create_kuka_kr5(opacity=0.7, color="gray", eef_frame_visible=False)
robot = Robot.create_abb_crb(opacity=0.7, color="gray", eef_frame_visible=False)
robot = Robot.create_epson_t6(opacity=0.7, color="gray", eef_frame_visible=False)

sim = Simulation([robot], load_screen_color="#191919", background_color="#222224", camera_type="orthographic",
                 show_world_frame=False, width=width, height=height)

# Create all objects that will be used during the simulation

far = Utils.trn([1000, 1000, 1000])


def clone_link_as_rigid_body(name, link):
    list_model_3d = []
    for model3d in link.list_model_3d:
        list_model_3d.append(
            Model3D(model3d.url, model3d.scale, model3d.htm, MeshMaterial(color="gold", opacity=0.8)))

    return RigidObject(list_model_3d, name=name, htm=far)


links_alternative = []
for i in range(len(robot.links)):
    links_alternative.append(clone_link_as_rigid_body("rigid_object_link_" + str(i), robot.links[i]))
    sim.add(links_alternative[-1])

htm_dh = robot.fkm(axis="dh")

htm = [robot.htm_base_0]
for i in range(len(robot.links)):
    htm.append(htm_dh[i])

x_axis = []
y_axis = []
z_axis = []

vector_length = 0.12

lines_purple = Cylinder(name="linePurple", htm=far, radius=0.002, height=2, color="purple")
lines_orange = Cylinder(name="lineOrange", htm=far, radius=0.002, height=2, color="#FFA500")
points_A = Ball(name="pointA", htm=far, radius=0.015, color="cyan")
points_B = Ball(name="pointB", htm=far, radius=0.015, color="green")

line_between_points = []
start_lines = []
end_lines = []
dist_between_points = 0.01

for i in range(len(robot.links)):
    p_A = (htm[i] @ Utils.trn([0, 0, robot.links[i].d]))[0:3, 3]
    p_B = htm[i + 1][0:3, 3]

    n_points = floor(np.linalg.norm(p_A - p_B) / dist_between_points)
    start_lines.append(len(line_between_points))

    for j in range(n_points):
        line_between_points.append((1 - j / n_points) * p_A + (j / n_points) * p_B)

    end_lines.append(len(line_between_points))

n = len(robot.links)
line_between_points = np.array(line_between_points).transpose()
if np.shape(line_between_points)[0]==0:
    line_between_points = np.zeros((3,0))

line_between_points_pc = PointCloud(name="lineBetweenPoints", points=line_between_points, size=2, color="white")
line_between_points_pc.add_ani_frame(0, 0, 0)

sim.add(lines_purple)
sim.add(lines_orange)
sim.add(points_A)
sim.add(points_B)
sim.add(line_between_points_pc)

for i in range(len(robot.links) + 1):
    x_axis.append(Cylinder(name="xAxis" + str(i), color="red", htm=far, radius=0.003, height=vector_length))
    y_axis.append(Cylinder(name="yAxis" + str(i), color="limegreen", htm=far, radius=0.003, height=vector_length))
    z_axis.append(Cylinder(name="zAxis" + str(i), color="blue", htm=far, radius=0.003, height=vector_length))

    sim.add(x_axis[-1])
    sim.add(y_axis[-1])
    sim.add(z_axis[-1])

style = "top:" + str(0.8 * height) + "px;right:" + str(0) + "px;width:" + str(
    width) + "px;position:absolute;text-align:center;color:white;background-color:#222224;font-smooth:always;font-family:arial"

explanation = HTMLDiv(html_text="", style=style)

sim.add(explanation)


def txt_link(i):
    return "<b>link<sub>" + str(i) + "</sub></b>"


def txt_frame(i):
    return "<b>F<sub>DH" + str(i) + "</sub></b>"


def txt_joint(i):
    return "<b>junta<sub>" + str(i) + "</sub></b>"


def txt_line_purple(i):
    return "<span style='color:#FF7AFF'><b>linha<sub>" + str(i) + "</sub></b></span>"


def txt_line_orange(i):
    return "<span style='color:#FFA500'><b>linha<sub>" + str(i) + "</sub></b></span>"


def txt_pointA(i):
    return "<span style='color:cyan'><b>ponto<sub>" + str(i) + "," + str(i + 1) + "</sub></b></span>"


def txt_pointB(i):
    return "<span style='color:#7bb572'><b>ponto<sub>" + str(i) + "," + str(i - 1) + "</sub></b></span>"


def txt_axis_x(i):
    return "<span style='color:red'><b>x<sub>DH" + str(i) + "</sub></b></span>"


def txt_axis_y(i):
    return "<span style='color:limegreen'><b>y<sub>DH" + str(i) + "</sub></b></span>"


def txt_axis_z(i):
    return "<span style='color:blue'><b>z<sub>DH" + str(i) + "</sub></b></span>"


# Make the animation
k = 0
dt = 0.01
deltak = 200

# Animate the creation of all DH frames
for i in range(len(robot.links) + 1):

    explanation.add_ani_frame(k * dt, html_text="Vamos criar agora o referencial " + txt_frame(i) + "...")

    if i > 0:
        k += 3 * deltak
        explanation.add_ani_frame(k * dt, html_text="Vamos desenhar " + txt_line_orange(
            i) + ". Essa é a linha alinhada com a junta " + txt_joint(i) + "</b>.")
        # Show the line_(i-1)
        lines_orange.add_ani_frame(k * dt, htm=htm[i - 1])

    # Show the line_i
    k += 3 * deltak
    if i < len(robot.links):
        explanation.add_ani_frame(k * dt, html_text="Vamos desenhar " + txt_line_purple(
            i + 1) + ". Essa é a linha alinhada com a junta " + txt_joint(i + 1) + "</b>.")
    else:
        explanation.add_ani_frame(k * dt, html_text="Não há " + txt_line_purple(
            i + 1) + ",pois não existe " + txt_joint(i + 1) + ". Então, podemos escolher " + txt_line_purple(
            i + 1) + " arbitrariamente. A escolhemos alinhada com a junta anterior.</span>...")

    lines_purple.add_ani_frame(k * dt, htm=htm[i])

    # Show the pointB_i and pointA_i
    k += 3 * deltak
    text = ""
    if i > 0:

        text += "Vamos desenhar " + txt_pointA(i) + ". Esse é o ponto na " + txt_line_orange(
            i) + " que é o mais próximo da " + txt_line_purple(i + 1) + ".<br>"

        points_A.add_ani_frame(k * dt, htm=htm[i - 1] @ Utils.trn([0, 0, robot.links[i - 1].d]))

        text += "Vamos desenhar " + txt_pointB(i + 1) + ". Esse é o ponto na " + txt_line_purple(
            i + 1) + " que é o mais próximo " \
                     "da " + txt_line_orange(i) + ".<br>"

        if i < len(robot.links) and abs(1 - abs(htm[i - 1][0:3, 2].transpose() @ htm[i][0:3, 2])) < 0.001:
            text += "Como as linhas " + txt_line_orange(
                i) + " e " + txt_line_purple(i + 1) + " são paralelas, existe infinitos pares de " + txt_pointA(
                i) + " e " + txt_pointB(i + 1) + " para escolher. Podemos escolher arbitrariamente.<br>"

    else:
        text += "Para o primeiro referencial, " + txt_pointB(
            i + 1) + " pode ser escolhido arbitrariamente contanto que esteja em " + txt_line_purple(i + 1) + ".<br>"

    text += "O centro de " + txt_frame(i) + " é " + txt_pointB(i + 1) + "."
    explanation.add_ani_frame(k * dt, html_text=text)

    points_B.add_ani_frame(k * dt, htm=htm[i])

    # Create the vector z_i
    k += 4 * deltak
    text = "O eixo " + txt_axis_z(i) + " tem que estar alinhado com " + txt_line_purple(i + 1) + ".<br>"
    if i < len(robot.links):
        text += "Nós podemos escolher entre as duas direções arbitrariamente (estamos definindo o sentido 'positivo' " \
                "de " + (
                    "rotação" if robot.links[i].joint_type == 0 else "translação") + " do eixo)."
    else:
        text += "Para o último eixo, mantemos a mesma direção do eixo z de antes."

    explanation.add_ani_frame(k * dt, html_text=text)
    z_axis[i].add_ani_frame(k * dt, htm=htm[i] @ Utils.trn([0, 0, vector_length / 2]))

    # Create the vector x_i
    k += 3 * deltak
    if i > 0:
        if start_lines[i - 1] == end_lines[i - 1]:
            explanation.add_ani_frame(k * dt, html_text="Nesse caso, " + txt_pointA(i) + " e " + txt_pointB(
                i + 1) + " são iguais. Então, podemos escolher os eixos " + txt_axis_x(
                i) + " arbitrariamente contanto que seja ortogonal à " + txt_line_orange(
                i) + " e " + txt_line_purple(i + 1) + ".")
        else:
            explanation.add_ani_frame(k * dt, html_text="O eixo " + txt_axis_x(i) + " precisa ir de " + txt_pointA(
                i) + " até " + txt_pointB(i + 1) + ".")

            for j in range(start_lines[i - 1], end_lines[i - 1]):
                k += round(0.05 * deltak)
                line_between_points_pc.add_ani_frame(k * dt, start_lines[i - 1], j)
    else:
        k += 3 * deltak
        explanation.add_ani_frame(k * dt,
                                  html_text="No primeiro referencial, " + txt_frame(
                                      0) + ", podemos escolher o eixo " + txt_axis_x(
                                      0) + " arbitrariamente, contanto que seja ortogonal ao " \
                                           "eixo " + txt_axis_z(0) + " .")

    k += deltak
    x_axis[i].add_ani_frame(k * dt, htm=htm[i] @ Utils.roty(3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
    line_between_points_pc.add_ani_frame(k * dt, 0, 0)

    # Create the vector y_i
    k += 3 * deltak
    explanation.add_ani_frame(k * dt,
                              html_text="O eixo " + txt_axis_y(i) + " é únicamente determinado pelos eixos " + txt_axis_x(
                                  i) + " e " + txt_axis_z(i) + " pela regra da mão direita.")
    y_axis[i].add_ani_frame(k * dt, htm=htm[i] @ Utils.rotx(-3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))

    # Erase the lines and points
    k += 3 * deltak
    points_A.add_ani_frame(k * dt, htm=far)
    points_B.add_ani_frame(k * dt, htm=far)
    lines_orange.add_ani_frame(k * dt, htm=far)
    lines_purple.add_ani_frame(k * dt, htm=far)
    k += deltak

    # Flash the link object
    if i > 0:
        explanation.add_ani_frame(k * dt, html_text="O referencial, " + txt_frame(
            i) + " está grudado ao elo piscando em <span style='color:gold'><b>amarelo</b></span>.<br>Portanto" \
                 ", qualquer junta que move o elo move esse referencial.")
        for j in range(10):
            k += floor(0.1 * deltak)
            links_alternative[i - 1].add_ani_frame(k * dt, robot.fkm(axis="dh")[i - 1])
            k += floor(0.1 * deltak)
            links_alternative[i - 1].add_ani_frame(k * dt, far)
    else:
        explanation.add_ani_frame(k * dt,
                                  html_text="O primeiro referencial " + txt_frame(
                                      0) + ", não está grudado a nenhum elo, ele é fixo.")
        k += 2 * deltak

    # Move the robot from joint 0 to i (not included)
    for j in range(1, i + 1):
        q = robot.q0

        explanation.add_ani_frame(k * dt,
                                  html_text="Quando a junta " + txt_joint(j) + " move, ela move " + txt_frame(i) + ".")

        for l in range(floor(0.5 * deltak)):
            q[j - 1] += (robot.joint_limit[j - 1][0] - robot.q0[j-1])/ (floor(0.5 * deltak) - 1)
            htm_i = robot.fkm(axis="dh", q=q)[i - 1]
            robot.add_ani_frame(k * dt, q=q)
            x_axis[i].add_ani_frame(k * dt, htm=htm_i @ Utils.roty(3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
            y_axis[i].add_ani_frame(k * dt,
                                    htm=htm_i @ Utils.rotx(-3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
            z_axis[i].add_ani_frame(k * dt, htm=htm_i @ Utils.trn([0, 0, vector_length / 2]))
            k += 1

        for l in range(deltak):
            q[j - 1] += (robot.joint_limit[j - 1][1] - robot.joint_limit[j - 1][0]) / (deltak - 1)
            robot.add_ani_frame(k * dt, q=q)
            htm_i = robot.fkm(axis="dh", q=q)[i - 1]
            x_axis[i].add_ani_frame(k * dt, htm=htm_i @ Utils.roty(3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
            y_axis[i].add_ani_frame(k * dt,
                                    htm=htm_i @ Utils.rotx(-3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
            z_axis[i].add_ani_frame(k * dt, htm=htm_i @ Utils.trn([0, 0, vector_length / 2]))
            k += 1

        for l in range(floor(0.5 * deltak)):
            q[j - 1] += -(robot.joint_limit[j - 1][1]- robot.q0[j-1]) / (floor(0.5 * deltak) - 1)
            robot.add_ani_frame(k * dt, q=q)
            htm_i = robot.fkm(axis="dh", q=q)[i - 1]
            x_axis[i].add_ani_frame(k * dt, htm=htm_i @ Utils.roty(3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
            y_axis[i].add_ani_frame(k * dt,
                                    htm=htm_i @ Utils.rotx(-3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
            z_axis[i].add_ani_frame(k * dt, htm=htm_i @ Utils.trn([0, 0, vector_length / 2]))
            k += 1

        k += deltak

    k += 2 * deltak
    if i < len(robot.links):
        if i > 0:
            explanation.add_ani_frame(k * dt,
                                      html_text="As juntas que estão para frente na cadeia cinemática não movem o elo, " \
                                                "e portanto não movem o referencial.")
            k += 3 * deltak
    else:
        explanation.add_ani_frame(k * dt, html_text="Como este é o último referencial, todas as juntas o movem.")
        k += 3 * deltak

    # Move the axis i+1 (if available)
    if i < len(robot.links):

        explanation.add_ani_frame(k * dt, html_text="A " + txt_joint(
            i + 1) + ", por exemplo, quando movida não move  " + txt_frame(
            i) + ". O mesmo é verdade para <b>junta<sub>i</sub></b> com i > " + str(i) + ".")

        q = robot.q0
        for l in range(floor(0.5 * deltak)):
            q[i] += (robot.joint_limit[i][0]  - robot.q0[i])/ (floor(0.5 * deltak) - 1)
            robot.add_ani_frame(k * dt, q=q)
            k += 1

        for l in range(deltak):
            q[i] += (robot.joint_limit[i][1] - robot.joint_limit[i][0]) / (deltak - 1)
            robot.add_ani_frame(k * dt, q=q)
            k += 1

        for l in range(floor(0.5 * deltak)):
            q[i] += -(robot.joint_limit[i][1]- robot.q0[i]) / (floor(0.5 * deltak) - 1)
            robot.add_ani_frame(k * dt, q=q)
            k += 1

    # Erase the axis
    k += deltak
    x_axis[i].add_ani_frame(k * dt, htm=far)
    y_axis[i].add_ani_frame(k * dt, htm=far)
    z_axis[i].add_ani_frame(k * dt, htm=far)

    k += deltak

    k += 1

# Show all DH frames for a while
k += deltak
for i in range(len(robot.links) + 1):
    x_axis[i].add_ani_frame(k * dt, htm=htm[i] @ Utils.roty(3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
    y_axis[i].add_ani_frame(k * dt, htm=htm[i] @ Utils.rotx(-3.14 / 2) @ Utils.trn([0, 0, vector_length / 2]))
    z_axis[i].add_ani_frame(k * dt, htm=htm[i] @ Utils.trn([0, 0, vector_length / 2]))

explanation.add_ani_frame(k * dt, "Terminado!")
sim.save("D:\\PycharmProjects\\aulas_manipuladores\\presentation\\images\\aula3","anim3")