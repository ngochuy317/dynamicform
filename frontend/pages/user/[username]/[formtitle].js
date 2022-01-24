import useSWR from 'swr'
import { useRouter } from 'next/router'
import FormData from "../../../components/FormData"
import { useEffect } from "react"

export default function Home() {
  const router = useRouter()
  const { username, formtitle } = router.query

  const fetcher = (url) => fetch(url).then((res) => res.json())
  const constructForm = useSWR('http://localhost:8080/api/', fetcher)
  const dataForm = useSWR(`http://localhost:8080/api/user/${username}/${formtitle}`, fetcher)
  if (constructForm.data && dataForm.data) {

    for (const property in constructForm.data.fields) {
        let temp = constructForm.data.fields[property].name
        if (constructForm.data.fields[property].typename == "FormInput") {
            constructForm.data.fields[property].value = dataForm.data[0][temp]
            constructForm.data.fields[property].readonly = ""
        }
        else if (constructForm.data.fields[property].typename == "FormCheckbox") {
            if (dataForm.data[0].Terms == true) {
                constructForm.data.fields[property].checked = "checked"
            }
        }
        else if (constructForm.data.fields[property].typename == "FormSelect") {

        }
        else if (constructForm.data.fields[property].typename == "FormTextarea") {
            constructForm.data.fields[property].value = dataForm.data[0][temp]
        }

    }
  }
  

  if ((constructForm.error) || (dataForm.error)) return <div>failed to load</div>
  if ((!constructForm.data) || (!dataForm.data)) return <div>loading...</div>
  return (
      <div>
     <FormData {...constructForm.data } />
     </div>
  );
}