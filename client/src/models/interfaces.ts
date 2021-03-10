export interface RequestResponse {
    data: any;
    success: boolean;
    errorMessage: string | null;
    errorCode: number | null;
}

export interface Movie {
    title: string;
    year: number;
}
