# OpenFOAM case builder for platoons

Hello there! This is our GUI app for creating OpenFOAM cases about vehicle platoons. I will guide you through the installation and a tutorial about it.

## Installation

The following tutorial assumes you have a fresh installation of Ubuntu 20.04, where Python 3 is present.

Install `pip`:

```
sudo apt install python3-pip
```

Add directory `.local/bin` to PATH, appending the following line to `bashrc`:

```
export PATH=$PATH:$HOME/.local/bin
```

Clone the repository and install it:

```
git clone https://github.com/andreastedile/openfoam-platoons.git
cd openfoam-platoons
pip3 install .
```

Create a directory to house STL files. For your convenience, you can copy the one in the repository.

```
cp -r stl/ ~/Documents/
```

Define an environment variable pointing to the directory:

```
export STL_DIR=$HOME/Documents/stl
```

Notice how the directory you just copied also contains a file with the reference measures of the STL files in the directory. If you add new STL files, remember to define their reference measures in the file, otherwise the app won't start.

You're almost there! You also need to [install OpenFOAM v7 itself](https://openfoam.org/download/7-ubuntu/). It is needed for a rather simple functionality, which I am working to implement directly in Python. Once this will be done, this dependency will not be needed anymore.

OpenFOAM v8 has recently been released, but it is not compatible with the cases produced by our app. We will try to catch up and update the repository.

## Usage

The app starts with a setup arranged for Ahmed body cases. Unless you want to work with Ahmed bodies only, you will need to modify many parameters which require some knowledge about CFD.

Create a directory to house the case, and launch the app:

```
mkdir case
cd case
ofp
```

The `View` menu allows to switch between various possible settings:

- ``Length``: Adjust the time steps of the simulation and the CPU cores that will be allocated to OpenFOAM. If you intend to run the case on your computer, you must not exceed the CPU's logical cores, otherwise OpenFOAM will crash.

- ``Turbulence``: Adjust the turbulence variables. The simulations use the k-ω SST turbulence model. You can specify the flow speed (in our case, the speed at which the platoon is traveling), the turbulence kinetic energy (k) and the turbulence specific dissipation rate (ω).

- ``Wind tunnel``: Adjust the coordinates (thus, the dimensions) of the wind tunnel. The figure depicts the OpenFOAM coordinate system. Later I will explain how to decide which these values.

  - The cases we are considering are symmetric, because the vehicles are centered along their line. It is thus sufficient to simulate a half of the domain only: this is why `Y min` is locked to zero. `Z min` is also to zero because the vehicles are attached to the ground.
  - Coordinates are positive or negative integers.
  - You can also adjust the parameters of the ground floor's boundary layer.

  ![screenshot](https://github.com/AdvancedNetworkingSystems/openfoam-platoons/blob/master/screenshot.png)

- ``Vehicles > Distance and STL``: Select the vehicles to simulate, their names, their types (i.e., their STL) and their distances. The *distance* of a vehicle is the gap from its predecessor.

  - Clicking on the eye icon makes a window containing the vehicles' coordinates appear. This allows to understand the space they occupy and, accordingly, decide the wind tunnel's coordinates.

- ``Vehicles > Refinement``: Adjust the refinement level of each vehicle's features and surface.

- ``Vehicles > Layers``: Adjust the parameters of each vehicle's boundary layer. 

- `Region refinement`: Define regions to be refined, their coordinates and the refinement level.

The `File` menu allows to save the case. Clicking ``Save`` makes a confirmation window appear. By closing the window, the app terminates and the cases is ready to be run.

To run the case:

```
./Allrun
```

## Tutorial

Let's create a case with two Ahmed bodies, with a gap of 1.43 m. As I already mentioned, the app starts with a setup arranged for them, therefore it should be easy! We chose the parameters according to the following [Simscale simulation](https://www.simscale.com/docs/validation-cases/aerodynamics-flow-around-the-ahmed-body/) (if you can't see all of them, [open the project](https://www.simscale.com/projects/gschiaffini/ahmed_body/) and scrutinize it).

Such setup seems to produce good results (read [Andrea's bachelor thesis](https://github.com/andreastedile/bachelor-thesis) if you are interested).

1. Open the app.

2. Go `Length` and adjust your CPU cores.

3. Go to `Vehicles > Distance and STL`. Add a new vehicle with distance 1.43 m.

4. Go to `Wind tunnel`. In Andrea's thesis, wind tunnel's coordinates were chosen as follows:

   `X min`:  ⌊first vehicle's `X min` - 3⌋. Since the first vehicle's `X min` is fixed to 0, then it is -3

   `X max`: ⌈last vehicle's `X max` + 7⌉ = 11

   `Y max`: 3

   `Z max`: 5

   - To determine vehicles' coordinates, use the eye icon as suggested before.

5. Go to `Region refinement`. Add a new region, and name it "Domain". Use the same coordinates of step 3, and use Refinement = 4.

   Add two other regions enclosing the vehicles. Use Refinement = 7. In Andrea's thesis, coordinates were chosen as follows:

   `X min`: the vehicle's `X min` - 0.1

   `X max`: the vehicle's `X max` + the vehicle's length.

   `Y max`: 0.294

   ` Z max`:  0.507

   Therefore, in the first region, set `X min` = -0.1, `X max` = 2.088; in the second region, set `X min` = 2.373, `X max` = 4.561.

6. Save the case.

7. Run the case, grab a coffee and wait for the simulation to stop.