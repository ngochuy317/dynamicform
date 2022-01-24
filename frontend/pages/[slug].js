import Form from "../components/Form";
// import { pages } from "../data";

export default function Index(props) {
    const { form } = props;
    return <Form {...form} />;
}

export async function getStaticPaths() {
    return {
        paths: [{ params: { slug: "contact-us-2024" } }],
        fallback: false
    }
}

export async function getStaticProps() {
    const res = await fetch('http://formservice:8081/contact-us-2024')
    const form = await res.json()

    return {
        props: {
            form,
        },
    }
}
