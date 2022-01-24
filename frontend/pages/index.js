import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import useSWR from 'swr'
import Form from "../components/Form";

export default function Home() {
  const fetcher = (url) => fetch(url).then((res) => res.json())
  const { data, error } = useSWR('http://localhost:8080/api/', fetcher)

  if (error) return <div>failed to load</div>
  if (!data) return <div>loading...</div>
  return <Form {...data} />;
}

// export async function getStaticProps() {
//   const res = await fetch('http://webservice:8080/api/')
//   const posts = await res.json()

//   return {
//     props: {
//       posts,
//     },
//   }
// }

