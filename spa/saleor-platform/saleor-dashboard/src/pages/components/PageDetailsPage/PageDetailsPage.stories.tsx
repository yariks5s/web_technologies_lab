import { fetchMoreProps } from "@saleor/fixtures";
import { PageErrorCode } from "@saleor/graphql";
import { PageData } from "@saleor/pages/components/PageDetailsPage/form";
import { page } from "@saleor/pages/fixtures";
import Decorator from "@saleor/storybook/Decorator";
import { storiesOf } from "@storybook/react";
import React from "react";

import PageDetailsPage, { PageDetailsPageProps } from "./PageDetailsPage";

const props: PageDetailsPageProps = {
  errors: [],
  loading: false,
  onAssignReferencesClick: () => undefined,
  onCloseDialog: () => undefined,
  onRemove: () => undefined,
  onSubmit: () => undefined,
  page,
  referencePages: [],
  referenceProducts: [],
  attributeValues: [],
  saveButtonBarState: "default",
  fetchAttributeValues: () => undefined,
  onAttributeSelectBlur: () => undefined,
  fetchMoreAttributeValues: fetchMoreProps,
};

storiesOf("Pages / Page details", module)
  .addDecorator(Decorator)
  .add("default", () => <PageDetailsPage {...props} />)
  .add("loading", () => (
    <PageDetailsPage {...props} loading={true} page={undefined} />
  ))
  .add("form errors", () => (
    <PageDetailsPage
      {...props}
      errors={([
        "title",
        "slug",
        "content",
        "publicationDate",
        "isPublished",
        "seoDescription",
        "seoTitle",
      ] as Array<keyof PageData>).map(field => ({
        __typename: "PageError",
        attributes: [],
        code: PageErrorCode.INVALID,
        field,
        message: "Page field error",
      }))}
    />
  ));
