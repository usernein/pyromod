import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import Heading from '@theme/Heading';
import styles from './index.module.css';
import {ChatSimulator} from "../components/ChatSimulator";
import {PyromodChatSimulator} from "../components/PyromodChatSimulator";
import {PyromodCodeBox} from "../components/PyromodCodeBox";

function HomepageHeader() {
    const {siteConfig} = useDocusaurusContext();
    return (
        <header className={clsx('hero hero--primary', styles.heroBanner)}>
            <div className="container">
                <Heading as="h1" className="hero__title">
                    {siteConfig.title}
                </Heading>
                <p className="hero__subtitle">{siteConfig.tagline}</p>
            </div>
        </header>
    );
}

export default function Home() {
    const {siteConfig} = useDocusaurusContext();

    const updateProcessor = (message) => {
        if (message === "/start") {
            return "Hello! I'm a bot.";
        }
        return "I don't understand.";
    }
    return (
        <Layout
            title={`Hello from ${siteConfig.title}`}
            description="Description will go into a meta tag in <head />">
            <HomepageHeader/>
            <main className={"flex flex-col md:flex-row w-full gap-5 justify-center items-center"}>
                <PyromodChatSimulator />
                <PyromodCodeBox />
            </main>
        </Layout>
    );
}
