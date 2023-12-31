import Decorator from "@saleor/storybook/Decorator";
import { storiesOf } from "@storybook/react";
import React from "react";

import TranslationsLanguageListPage, {
  TranslationsLanguageListPageProps,
} from ".";
import { languages } from "../../fixtures";

const props: TranslationsLanguageListPageProps = {
  languages,
};

storiesOf("Translations / Language list", module)
  .addDecorator(Decorator)
  .add("default", () => <TranslationsLanguageListPage {...props} />)
  .add("loading", () => (
    <TranslationsLanguageListPage {...props} languages={undefined} />
  ))
  .add("no data", () => (
    <TranslationsLanguageListPage {...props} languages={[]} />
  ));
