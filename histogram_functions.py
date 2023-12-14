import numpy as np


def state_state(data_frame, steps, states):
    st = [None] * (steps + 1)
    res = np.full((4,) * (steps + 1), True, dtype=object)
    num = np.full((4,) * (steps + 1), 0, dtype=int)

    for s in range(len(st)):
        st[s] = np.full((4,) * (len(st) - s), "place holder", dtype=object)
    st[-1] = st[-1][np.newaxis, :]

    for i in range(len(data_frame) - steps):
        for idx, s in enumerate(np.arange(i, i + (steps + 1))):
            temp_list = list(zip(states, st[idx]))

            if idx == (len(st) - 1):
                st[idx] = np.tile(data_frame.iloc[s, 3], len(states)) == states
                st[idx] = st[idx][np.newaxis, :]

                for a2 in range(0, len(st), 1):
                    res = res & st[a2]

            else:
                for k in range(len(states)):
                    temp_list[k][1][:] = (
                        np.tile(data_frame.iloc[s, 3], len(states)) == states
                    )[k]

        num = num + res.astype(int)
        res[:] = True
    return num


def hidden_observable(
    data_frame, steps, h_states, o_states, hidden_col_idx, observations_col_idx
):
    st = [None] * (steps + 1)
    res = np.full((len(h_states),) * (steps + 1), True, dtype=object)
    num = np.full((len(h_states),) * (steps + 1) + (len(o_states),), 0, dtype=int)
    obs = np.full(
        (len(h_states),) * (steps + 1) + (len(o_states),), "place holder", dtype=object
    )
    observations = np.full((1, len(o_states)), "place holder", dtype=object)

    for s in range(len(st)):
        st[s] = np.full((len(h_states),) * (len(st) - s), "place holder", dtype=object)
    st[-1] = st[-1][np.newaxis, :]

    for i in range(len(data_frame) - steps):
        for idx, s in enumerate(np.arange(i, i + (steps + 1))):
            temp_list = list(zip(h_states, st[idx]))

            if idx == (len(st) - 1):
                st[idx] = (
                    np.tile(data_frame.iloc[s, hidden_col_idx], len(h_states))
                    == h_states
                )
                st[idx] = st[idx][np.newaxis, :]

                for a2 in range(0, len(st), 1):
                    res = res & st[a2]

                observations = (
                    np.tile(data_frame.iloc[s, observations_col_idx], len(o_states))
                    == o_states
                )

                obs = np.tile(res.reshape(res.shape + (1,)), len(o_states))
                obs = obs & observations

            else:
                for k in range(len(h_states)):
                    temp_list[k][1][:] = (
                        np.tile(data_frame.iloc[s, hidden_col_idx], len(h_states))
                        == h_states
                    )[k]

        num = num + obs.astype(int)
        res[:] = True
        obs[:] = "place holder"
    return num
