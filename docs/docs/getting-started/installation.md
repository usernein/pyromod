---
title: Installation
sidebar_position: 2
---

To get started with pyromod, you can install it using pip:

```bash
pip install pyromod
```

Or poetry:

```bash
poetry add pyromod
```

Or rye:

```bash
rye add pyromod
```
:::note

pyromod **requires** pyrogram to be installed, since it's a plugin that only does monkeypatching, rather than a standalone fork of pyrogram.

:::

:::info

You can use pyromod natively if you are using Hydrogram instead of Pyrogram, since Hydrogram is a (hugely optimized) fork of Pyrogram that already includes pyromod built-in.

:::