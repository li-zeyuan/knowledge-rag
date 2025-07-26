import axios from 'axios'

export function chatWithLLm(data: any) {
    return axios.post('/api/chat/with_llm', data).then(res => {
        return res.data
    })
}