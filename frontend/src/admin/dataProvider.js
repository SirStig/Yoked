import { fetchUtils } from "react-admin";
import { stringify } from "query-string";

// Set up the API URL
const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api/admin";

// Wrapper for HTTP client with custom authorization
const httpClient = (url, options = {}) => {
  const token = localStorage.getItem("adminToken");
  if (!options.headers) {
    options.headers = new Headers({ Accept: "application/json" });
  }
  if (token) {
    options.headers.set("Authorization", `Bearer ${token}`);
  } else {
    console.warn("No admin token found for request.");
  }
  return fetchUtils.fetchJson(url, options);
};

// Define the data provider for React Admin
const dataProvider = {
  getList: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const { field, order } = params.sort;
    const query = {
      ...fetchUtils.flattenObject(params.filter),
      _sort: field,
      _order: order,
      _start: (page - 1) * perPage,
      _end: page * perPage,
    };
    const url = `${API_URL}/${resource}?${stringify(query)}`;

    try {
      const { headers, json } = await httpClient(url);
      return {
        data: json,
        total: parseInt(headers.get("X-Total-Count"), 10),
      };
    } catch (error) {
      console.error(`Failed to fetch list for resource "${resource}"`, error);
      throw error;
    }
  },

  getOne: async (resource, params) => {
    const url = `${API_URL}/${resource}/${params.id}`;
    try {
      const { json } = await httpClient(url);
      return { data: json };
    } catch (error) {
      console.error(`Failed to fetch resource "${resource}" with id "${params.id}"`, error);
      throw error;
    }
  },

  getMany: async (resource, params) => {
    const query = {
      id: params.ids,
    };
    const url = `${API_URL}/${resource}?${stringify(query)}`;
    try {
      const { json } = await httpClient(url);
      return { data: json };
    } catch (error) {
      console.error(`Failed to fetch many resources for "${resource}"`, error);
      throw error;
    }
  },

  getManyReference: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const { field, order } = params.sort;
    const query = {
      ...fetchUtils.flattenObject(params.filter),
      [params.target]: params.id,
      _sort: field,
      _order: order,
      _start: (page - 1) * perPage,
      _end: page * perPage,
    };
    const url = `${API_URL}/${resource}?${stringify(query)}`;
    try {
      const { headers, json } = await httpClient(url);
      return {
        data: json,
        total: parseInt(headers.get("X-Total-Count"), 10),
      };
    } catch (error) {
      console.error(`Failed to fetch many references for "${resource}"`, error);
      throw error;
    }
  },

  update: async (resource, params) => {
    const url = `${API_URL}/${resource}/${params.id}`;
    try {
      const { json } = await httpClient(url, {
        method: "PUT",
        body: JSON.stringify(params.data),
      });
      return { data: json };
    } catch (error) {
      console.error(`Failed to update resource "${resource}" with id "${params.id}"`, error);
      throw error;
    }
  },

  updateMany: async (resource, params) => {
    const url = `${API_URL}/${resource}`;
    try {
      const { json } = await httpClient(url, {
        method: "PUT",
        body: JSON.stringify({ ids: params.ids, data: params.data }),
      });
      return { data: json };
    } catch (error) {
      console.error(`Failed to update many resources for "${resource}"`, error);
      throw error;
    }
  },

  create: async (resource, params) => {
    const url = `${API_URL}/${resource}`;
    try {
      const { json } = await httpClient(url, {
        method: "POST",
        body: JSON.stringify(params.data),
      });
      return { data: { ...params.data, id: json.id } };
    } catch (error) {
      console.error(`Failed to create resource "${resource}"`, error);
      throw error;
    }
  },

  delete: async (resource, params) => {
    const url = `${API_URL}/${resource}/${params.id}`;
    try {
      const { json } = await httpClient(url, {
        method: "DELETE",
      });
      return { data: json };
    } catch (error) {
      console.error(`Failed to delete resource "${resource}" with id "${params.id}"`, error);
      throw error;
    }
  },

  deleteMany: async (resource, params) => {
    const url = `${API_URL}/${resource}`;
    try {
      const { json } = await httpClient(url, {
        method: "DELETE",
        body: JSON.stringify({ ids: params.ids }),
      });
      return { data: json };
    } catch (error) {
      console.error(`Failed to delete many resources for "${resource}"`, error);
      throw error;
    }
  },
};

export default dataProvider;
