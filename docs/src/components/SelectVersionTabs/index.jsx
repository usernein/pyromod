import {useState} from "react";
import clsx from "clsx";

export const SelectVersionTabs = () => {
    const [activeTab, setActiveTab] = useState(0);

    const genOnClick = (index) => {
        return () => {
            setActiveTab(index);
        }
    }

    const genClassName = (index) => {
        return clsx("tab", {
            "tab-active": activeTab === index
        })
    }

    return (
        <div role="tablist" className="tabs tabs-boxed">
            <a role="tab" className={genClassName(0)} onClick={genOnClick(0)}>Without pyromod</a>
            <a role="tab" className={genClassName(1)} onClick={genOnClick(1)}>With pyromod</a>
        </div>
    );
}