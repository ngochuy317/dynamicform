import Head from 'next/head'
import Image from 'next/image'
import styles from '../../styles/Home.module.css'
import useSWR from 'swr'
import Link from 'next/link'

export default function Home() {
  const fetcher = (url) => fetch(url).then((res) => res.json())
  const { data, error } = useSWR('http://localhost:8080/api/user', fetcher)
  console.log(data)

  if (error) return <div>failed to load</div>
  if (!data) return <div>loading...</div>
  return (
    <div>
        {data.map(user=>(
            <Link href={`/user/${user.username}`}>
            <label><li>{user.username}</li></label>
            </Link>
        )
        )}
    </div>
  );
}