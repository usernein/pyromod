## Initializing pyromod

To initialize pyromod, on the file that creates the client instance, simply import the Client class from pyromod instead
of pyrogram:

```python
from pyromod import Client
```

And that's all! You can still use the `Client` class as you would normally do with Pyrogram, but now having all the
extra features.

>You don't need to change the imports on the plugins files. Even by importing `Client` from pyrogram, the pyromod  features will be available anyway.

>In order to monkeyatch pyromod features successfully, it's just required that the  first `Client` class imported to your project code should be from pyromod. Then all the other future `Client` instances  will be patched automatically.

>On custom plugins, you just need to import Client from pyromod if you want your IDE to recognize and suggest
the extra features based on `pyromod.Client` type.
