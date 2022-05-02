export function createSearchUrl(
  searchText,
  phraseSearch,
  filterDateFrom,
  filterDateTo
) {
  const base = "http://localhost:8000/documents/search/";
  const search_string = searchText ? `search_string=${searchText}` : "";
  const phrase_search = phraseSearch ? `&phrase_search=${phraseSearch}` : "";
  const date_from = filterDateFrom ? `&end_date=${filterDateFrom}` : "";
  const date_to = filterDateTo ? `&start_date=${filterDateTo}` : "";
  const url = `${base}?${search_string}${phrase_search}${date_from}${date_to}`;
  return url;
}

export function searchRequest(searchUrl, onSuccess, onFail) {
  let url = encodeURI(searchUrl);

  let successeFullFetch = true;
  let jsonData = {};
  let errorMessage = "";

  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  })
    .then((response) => {
      if (!response?.ok) {
        // Throws the status code of error to be caught in the catch statement
        throw response?.status;
      } else {
        return response.json();
      }
    })
    .then((responseJson) => {
      jsonData = responseJson;
    })
    .catch((error) => {
      successeFullFetch = false;

      // If an error is thrown it will be caught and handeled here.
      // Depending on the error the correct error message will be set
      console.log(error);
      if (error >= 500) {
        // Handle server errors
        errorMessage = "Server error";
      } else if (error >= 400) {
        // Handle client errors
        errorMessage = "Client error";
      } else {
        // Handle Unknown errors
        errorMessage = "Unknown error";
      }
    })
    .finally(() => {
      // If errors were caugh while fetching the onError with correct errorMessage will be executed
      // otherwise onSuccess functionw with fetched json data
      console.log(jsonData);
      console.log(errorMessage);
      return successeFullFetch ? onSuccess(jsonData) : onFail(errorMessage);
    });
}

export const YEAR_VECTOR = [
  2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010,
  2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997,
  1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984,
  1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971,
  1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958,
  1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945,
  1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932,
  1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919,
  1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906,
  1905, 1904, 1903, 1902, 1901, 1900,
];

// https://coolors.co/cfdbd5-e8eddf-373d20-7b9aa3-242423
export const COLOURS = {
    base: "#CFDBD5",
    lightBase: "#E8EDDF",
    darkText: "#242423",
    primaryColour: "#373D20",
    secondaryColour: "#7B9AA3",

}