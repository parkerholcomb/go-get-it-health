export const sendPrompt = async (phone) => {
    const resp = await requestApi('/sms/prompt', 'POST', { 'phone': phone })
    console.log(resp)
    return resp
}

export const requestApi = async (
    path = '',
    method = 'GET',
    data = null,
    headers = {}) => {
  
    const baseAPI = 'https://5x53zttjo2.execute-api.us-east-1.amazonaws.com'
    // Check if API URL has been set -- I set it above
    // if (!config?.domains?.api) {
    //   throw new Error(`Error: Missing API Domain – Please add the API domain from your serverless Express.js back-end to this front-end application.  You can do this in the "site" folder, in the "./config.js" file.  Instructions are listed there and in the documentation.`)
    // }
  
    // Prepare URL
    if (!path.startsWith('/')) {
      path = `/${path}`
    }
    const url = `${baseAPI}${path}`
  
    // Set headers
    headers = Object.assign(
      { 'Content-Type': 'application/json' },
      headers
    )
  
    // Default options are marked with *
    const response = await fetch(url, {
      method: method.toUpperCase(),
      mode: 'no-cors',
      cache: 'no-cache',
      headers,
      body: data ? JSON.stringify(data) : null
    })
  
    if (response.status < 200 || response.status >= 300) {
      const error = await response.json()
      throw new Error(error.error)
    }
  
    return await response.json()
  }