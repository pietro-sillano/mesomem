# How to use it
These two scripts are used to generate membrane initial configurations used in the example.

### Planar lattice `planar_lattice.py`
Creates a flat membrane by placing particles on a NxN hexagonal grid with inter-particle distance d with (or without) periodic boundary conditions.

```bash
python planar_lattice.py --path /home/pietro/test --N 50 --d 0.85 --PBC
```

### Spherical vesicle (spherical_vesicle.py)
Creates a sphere by placing particles on the vertices of an icosphere. You can choose the number of particles accordingly to the iteration number.  The script will output the predicted radius for you. It scales the resulting sphere so that the average distance between neighboring particles matches the correct distance for the model: d = 0.8-0.85


```bash
python spherical_vesicle.py
```
