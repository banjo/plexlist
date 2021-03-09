<template>
    <div class="home">
        <div class="container">
            <div class="progress-container">
                <div class="progress" :style="progressStyle"></div>
                <div
                    v-for="step in steps"
                    :key="step"
                    class="circle"
                    :class="{ active: step <= current }"
                >
                    {{ step }}
                </div>
            </div>

            <div class="action-container">
                <div class="input-fields" v-if="current === 1">
                    <h1>Login</h1>
                    <input
                        class="input"
                        type="email"
                        name="email"
                        id="email"
                        placeholder="Email..."
                        v-model="username"
                    />
                    <input
                        class="input"
                        type="password"
                        name="password"
                        id="password"
                        placeholder="Password..."
                        v-model="password"
                    />
                </div>

                <div v-if="current === 2" class="input-fields">
                    <h1>Select server</h1>

                    <select
                        class="form-select form-select-lg"
                        aria-label=".form-select-lg example"
                        v-model="selectedServer"
                    >
                        <option selected value="">Select server</option>
                        <option
                            v-for="(server, index) in servers"
                            :key="index"
                            :value="server"
                        >
                            {{ server }}
                        </option>
                    </select>
                </div>

                <div v-if="current === 3" class="input-fields">
                    <h1>Select IMDB list</h1>

                    <input
                        class="input"
                        type="text"
                        name="imdb"
                        id="imdb"
                        placeholder="IMDb ID..."
                        v-model="imdb"
                    />
                </div>

                <div v-if="current === 4" class="input-fields">
                    <h1>Playlist</h1>

                    <button
                        type="button"
                        class="btn secondary"
                        data-toggle="modal"
                        data-target="#movieModal"
                    >
                        See all movies
                    </button>

                    <input
                        class="input"
                        type="text"
                        name="playlist"
                        id="playlist"
                        placeholder="Playlist name..."
                        v-model="playlist"
                    />

                    <div class="m-4">
                        <h3>Users</h3>
                        <div
                            class="form-check left-align"
                            v-for="(user, index) of users"
                            :key="index"
                        >
                            <input
                                class="form-check-input"
                                type="checkbox"
                                :value="user"
                                id="flexCheckDefault"
                                v-model="selectedUsers"
                            />
                            <label
                                class="form-check-label"
                                for="flexCheckDefault"
                            >
                                {{ user }}
                            </label>
                        </div>
                    </div>
                </div>
            </div>

            <div class="error-container">
                <div v-if="errorMessage" class="error-message">
                    {{ errorMessage }}
                </div>
            </div>

            <button class="btn" @click="prev" :disabled="prevDisabled">
                Prev
            </button>
            <button class="btn" @click="next" :disabled="nextDisabled">
                Next
                <span
                    v-if="loading"
                    class="spinner-border spinner-border-sm"
                    role="status"
                    aria-hidden="true"
                ></span>
            </button>
        </div>

        <!-- Modal -->
        <div
            class="modal fade"
            id="movieModal"
            tabindex="-1"
            role="dialog"
            aria-labelledby="movieModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="movieModalLabel">Movies</h5>
                        <button
                            type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                        >
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <ul class="list-group">
                            <li
                                class="list-group-item"
                                v-for="(movie, index) of movies"
                                :key="index"
                            >
                                {{ movie.title }} ({{ movie.year }})
                            </li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-dismiss="modal"
                        >
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import {
    addMovies,
    chooseServer,
    getServers,
    getUsers,
    login,
    scrapeImdb,
} from "../services/request-service";
import { RequestResponse } from "../models/interfaces";

@Component({
    components: {},
})
export default class Home extends Vue {
    steps = 5;
    current = 4;
    loading = false;

    username = "";
    password = "";
    servers = [];
    selectedServer = "";
    imdb = "";
    movies = [
        {
            title: "Inception",
            year: 2008,
        },
    ];
    playlist = "";
    users = [
        "albin.tystrand@gmail.com",
        "corderoy.pihl@gmail.com",
        "daave.olsson@gmail.com",
        "emhj0516@fridaskolan.se",
        "emilsvensson99@hotmail.com",
        "Evelina.odman@gmail.com",
        "harald.brandelius@gmail.com",
        "Jacob.c.westman@gmail.com",
        "johaan.westerlund@gmail.com",
        "rob.trollhattan@gmail.com",
        "sarajuliawestman@gmail.com",
        "stuganibokenaset@gmail.com",
        "viktor@kopperod.se",
    ];
    selectedUsers = [];

    errorMessage = "";

    get progressStyle() {
        return `width: ${((this.current - 1) / (this.steps - 1)) * 100}%`;
    }

    get prevDisabled() {
        return this.current === 1;
    }

    get nextDisabled() {
        return this.current === this.steps;
    }

    async next() {
        this.errorMessage = "";
        this.loading = true;

        console.log(this.selectedUsers);

        // login
        if (this.current === 1) {
            const response = (await login(
                this.username,
                this.password
            )) as RequestResponse;

            if (!response.success) {
                this.errorMessage = response.errorMessage!;
                this.loading = false;
                return;
            }

            const servers = (await getServers()) as RequestResponse;

            if (!servers.success) {
                this.errorMessage = response.errorMessage!;
                this.loading = false;
                return;
            }

            this.servers = servers.data;
        } else if (this.current === 2) {
            // select server
            if (this.selectedServer === "") {
                this.loading = false;
                return;
            }

            await chooseServer(this.selectedServer);
        } else if (this.current === 3) {
            // scrape imdb and choose users
            if (!this.imdb) {
                this.loading = false;
                return;
            }

            const response = (await scrapeImdb(this.imdb)) as RequestResponse;

            if (!response.success) {
                this.errorMessage = response.errorMessage!;
                this.loading = false;
                return;
            }

            const users = (await getUsers()) as RequestResponse;

            if (!users.success) {
                this.errorMessage = response.errorMessage!;
                this.loading = false;
                return;
            }

            this.users = users.data;
            this.movies = response.data;
        } else if (this.current === 4) {
            // add movies
            const response = (await addMovies(
                this.movies,
                this.playlist,
                this.users
            )) as RequestResponse;

            if (!response.success) {
                this.errorMessage = response.errorMessage!;
                this.loading = false;
                return;
            }

            console.log(response);
        }

        this.current++;
        this.loading = false;
        if (this.current > this.steps) {
            this.current = this.steps;
        }
    }
    prev() {
        this.current--;
        if (this.current < 1) {
            this.current = 1;
        }
    }
}
</script>

<style>
.action-container {
    margin-top: var(--size-large1);
    margin-bottom: var(--size-large1);
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.input-fields {
    display: flex;
    flex-direction: column;
    width: 70%;
}

.input {
    margin-top: var(--size-medium1);
    height: var(--size-large2);
    border-radius: var(--radius);
    padding-left: var(--size-medium1);
    border: 0;
    font-family: inherit;
    font-size: inherit;
}

.error-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

.error-message {
    margin: var(--size-small1) 0;
    padding: var(--size-small3);
    border-radius: var(--radius);
    color: #d8000c;
    background-color: #ffbaba;
    width: 70%;
}

.modal-dialog {
    color: black;
}

.left-align {
    text-align: left;
}

:root {
    --line-border-fill: var(--clr-primary);
    --line-border-empty: var(--clr-gray500);
}

body {
    background-color: var(--clr-dark);
    color: var(--clr-light);
    font-family: "Muli", sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    overflow: hidden;
    margin: 0;
}

.container {
    text-align: center;
}

.progress-container {
    display: flex;
    justify-content: space-between;
    position: relative;
    margin-bottom: 30px;
    max-width: 100%;
    width: 350px;
}

.progress-container::before {
    content: "";
    background-color: var(--line-border-empty);
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    height: 3px;
    width: 100%;
    z-index: -1;
}

.progress {
    background-color: var(--line-border-fill);
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    height: 3px;
    width: 0%;
    z-index: -1;
    transition: 0.3s ease;
}

.circle {
    background-color: #fff;
    color: #999;
    border-radius: 50%;
    height: 30px;
    width: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid var(--line-border-empty);
    transition: 0.3s ease 0.1s;
}

.circle.active {
    border-color: var(--line-border-fill);
}

.btn {
    background-color: var(--line-border-fill);
    color: #fff;
    border: 0;
    border-radius: var(--radius);
    cursor: pointer;
    font-family: inherit;
    padding: 8px 30px;
    padding: var(--size-small3) var(--size-large1);
    margin: var(--size-small3);
    font-size: inherit;
    transition: 0.1s;
}

.secondary {
    background-color: var(--clr-secondary);
}

.btn:active {
    transform: translateY(1px);
}

.btn:focus {
    outline: 0;
}

.btn:disabled {
    background-color: var(--line-border-empty);
    cursor: not-allowed;
}
</style>