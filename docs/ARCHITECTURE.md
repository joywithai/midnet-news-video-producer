# Architecture

```text
brief.md + audio + src/
        |
        v
Brief Validator -> SRT Aligner -> Asset Inventory -> Scene/Card Renderer
                                                   |             |
                                                   v             v
                                             Source Record   MP4 + Thumbnails
                                                   \             /
                                                    Final Media QC
                                                          |
                                                          v
                                                     production/
```

The CLI is deterministic and can be invoked by any AI agent that can clone a repository and run terminal commands.
