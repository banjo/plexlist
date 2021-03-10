import { Movie, RequestResponse } from "@/models/interfaces";
import axios from "axios";

const URL = "http://localhost:5000";

const instance = axios.create({
    withCredentials: true,
    baseURL: URL,
});

export const login = async (
    username: string,
    password: string
): Promise<RequestResponse> => {
    try {
        const response = await instance.post(`/sign-in`, {
            username,
            password,
        });
        const requestResponse: RequestResponse = {
            data: response.data,
            errorCode: null,
            errorMessage: null,
            success: true,
        };
        return requestResponse;
    } catch (error) {
        const requestResponse: RequestResponse = {
            data: null,
            errorCode: error.response.status,
            errorMessage: error.response.data.error,
            success: false,
        };

        return requestResponse;
    }
};

export const getServers = async (): Promise<RequestResponse> => {
    try {
        const response = await instance.get(`/get-servers`);

        const requestResponse: RequestResponse = {
            data: response.data,
            errorCode: null,
            errorMessage: null,
            success: true,
        };
        return requestResponse;
    } catch (error) {
        const requestResponse: RequestResponse = {
            data: null,
            errorCode: error.response.status,
            errorMessage: error.response.data.error,
            success: false,
        };

        return requestResponse;
    }
};

export const chooseServer = async (
    server: string
): Promise<RequestResponse> => {
    try {
        const response = await instance.post(`/choose-server`, {
            server,
        });

        const requestResponse: RequestResponse = {
            data: response.data,
            errorCode: null,
            errorMessage: null,
            success: true,
        };
        return requestResponse;
    } catch (error) {
        const requestResponse: RequestResponse = {
            data: null,
            errorCode: error.response.status,
            errorMessage: error.response.data.error,
            success: false,
        };

        return requestResponse;
    }
};

export const scrapeImdb = async (id: string): Promise<RequestResponse> => {
    try {
        const response = await instance.post(`/scrape-imdb`, {
            id,
        });

        const requestResponse: RequestResponse = {
            data: response.data,
            errorCode: null,
            errorMessage: null,
            success: true,
        };
        return requestResponse;
    } catch (error) {
        const requestResponse: RequestResponse = {
            data: null,
            errorCode: error.response.status,
            errorMessage: error.response.data.error,
            success: false,
        };

        return requestResponse;
    }
};

export const getUsers = async (): Promise<RequestResponse> => {
    try {
        const response = await instance.get(`/get-users`);

        const requestResponse: RequestResponse = {
            data: response.data,
            errorCode: null,
            errorMessage: null,
            success: true,
        };
        return requestResponse;
    } catch (error) {
        const requestResponse: RequestResponse = {
            data: null,
            errorCode: error.response.status,
            errorMessage: error.response.data.error,
            success: false,
        };

        return requestResponse;
    }
};

export const addMovies = async (
    movies: Movie[],
    name: string,
    users: string[]
): Promise<RequestResponse> => {
    try {
        const response = await instance.post(`/add-movies`, {
            movies,
            name,
            users,
        });

        const requestResponse: RequestResponse = {
            data: response.data,
            errorCode: null,
            errorMessage: null,
            success: true,
        };
        return requestResponse;
    } catch (error) {
        const requestResponse: RequestResponse = {
            data: null,
            errorCode: error.response.status,
            errorMessage: error.response.data.error,
            success: false,
        };

        return requestResponse;
    }
};
