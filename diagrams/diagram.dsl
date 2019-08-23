# DEFINITIONS

[a] := "Off State"                   # Inside rectangle
(b) := "On State"                    # Inside rounded rectangle
/c/ := "Transition State"            # Inside Parallelogram


# Rules

# Horizontal layout
a -> b -> c
["next state"] -> a  # This affects the layout since it introduces branch
("new state") -> b  # This affects the layout since it introduces branch

/"curr state"/ -> c


# Vertical layout
a |> b |> c
/"another state"/ |> a
["state"] |> c