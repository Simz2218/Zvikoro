import axios from "axios";
import dayjs from "dayjs";
import { useContext, useState, useRef } from "react";
import AuthContext from "../context/AuthContext";

const baseURL = "http://127.0.0.1:8000/schools/";

const useAxios = () => {
  const { authTokens, setUser, setAuthTokens } = useContext(AuthContext);
  const [error, setError] = useState(null);
  const prevDataRef = useRef(null);

  const axiosInstance = axios.create({
    baseURL,
    headers: { Authorization: `Bearer ${authTokens?.access}` },
  });

  axiosInstance.interceptors.request.use(async (req) => {
    if (!authTokens) return req;

    const user = JSON.parse(atob(authTokens.access.split(".")[1]));
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

    if (!isExpired) return req;

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/schools/token/refresh/",
        {
          refresh: authTokens.refresh,
        }
      );
      localStorage.setItem("authTokens", JSON.stringify(response.data));
      setAuthTokens(response.data);
      setUser(JSON.parse(atob(response.data.access.split(".")[1])));

      req.headers.Authorization = `Bearer ${response.data.access}`;
      setError(null); // Clear the error
    } catch (error) {
      console.error("Error refreshing token:", error);
      setError(error); // Set the error
      return Promise.reject(error);
    }
    return req;
  });

  const getData = async () => {
    try {
      const response = await axiosInstance.get("User/");
      if (
        !prevDataRef.current ||
        JSON.stringify(prevDataRef.current) !== JSON.stringify(response.data)
      ) {
        prevDataRef.current = response.data;
        return response.data;
      }
      return prevDataRef.current;
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(error); // Set the error
      throw error;
    }
  };

  return { axiosInstance, getData, error };
};

export default useAxios;
