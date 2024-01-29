import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import Heading from '@theme/Heading';
import styles from './index.module.css';
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
            title={`pyromod documentation`}
            description="Powerful add-on that monkeypatches extra useful features on Pyrogram.">
            <HomepageHeader/>
            <main className={"flex flex-col items-center justify-center"}>
                <div className={"flex flex-col gap-5 justify-center items-center w-full"}>
                    <div className={"flex w-full flex-col md:flex-row justify-evenly items-center p-8 gap-5"}>
                        <section className={styles.advantage}>
                            Powerful add-on that monkeypatches extra useful features.
                        </section>
                        <section className={styles.advantage}>
                            Get user responses (or button clicks) effortlessly with a single line of code.
                        </section>
                        <section className={styles.advantage}>
                            Create keyboard-based interfaces for your bots with ease and fun.
                        </section>
                        <section className={styles.advantage}>
                            Effortlessly send messages with inline keyboards from your userbots.
                        </section>
                    </div>
                </div>
                <div className={"flex w-full flex-col-reverse md:flex-row gap-8 justify-center items-center"}>
                    <PyromodChatSimulator/>
                    <PyromodCodeBox/>
                </div>
                <a
                    href="/getting-started/intro"
                    className={"no=underline m-5"}
                >
                    <div
                        className={"no-underline hover:no-underline p-3 font-bold text-[var(--ifm-font-color-base-inverse)] bg-[var(--ifm-color-primary-light)] uppercase rounded-btn md:hover:brightness-90 duration-150 md:active:scale-95 select-none cursor-pointer"}>Get
                        Started
                    </div>
                </a>
            </main>
        </Layout>
    );
}
