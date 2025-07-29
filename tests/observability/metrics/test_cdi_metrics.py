import pytest

from tests.observability.metrics.constants import KUBEVIRT_CDI_IMPORT_PODS_HIGH_RESTART
from tests.observability.metrics.utils import expected_metric_labels_and_values, get_metric_labels_non_empty_value
from tests.observability.utils import validate_metrics_value
from utilities.constants import CDI_OPERATOR


@pytest.mark.polarion("CNV-10557")
def test_kubevirt_cdi_clone_pods_high_restart(
    skip_test_if_no_filesystem_sc,
    skip_test_if_no_block_sc,
    prometheus,
    zero_clone_dv_restart_count,
    restarted_cdi_dv_clone,
):
    validate_metrics_value(
        prometheus=prometheus,
        expected_value="1",
        metric_name="kubevirt_cdi_clone_pods_high_restart",
    )


@pytest.mark.polarion("CNV-10717")
@pytest.mark.s390x
def test_kubevirt_cdi_upload_pods_high_restart(
    prometheus,
    zero_upload_dv_restart_count,
    restarted_cdi_dv_upload,
):
    validate_metrics_value(
        prometheus=prometheus,
        expected_value="1",
        metric_name="kubevirt_cdi_upload_pods_high_restart",
    )


@pytest.mark.polarion("CNV-11744")
@pytest.mark.s390x
def test_metric_kubevirt_cdi_storageprofile_info(prometheus, storage_class_labels_for_testing):
    expected_metric_labels_and_values(
        values_from_prometheus=get_metric_labels_non_empty_value(
            prometheus=prometheus,
            metric_name=f"kubevirt_cdi_storageprofile_info"
            f"{{storageclass='{storage_class_labels_for_testing['storageclass']}'}}",
        ),
        expected_labels_and_values=storage_class_labels_for_testing,
    )


@pytest.mark.parametrize(
    "scaled_deployment",
    [
        pytest.param(
            {"deployment_name": CDI_OPERATOR, "replicas": 0},
            marks=(pytest.mark.polarion("CNV-11722")),
            id="Test_kubevirt_cdi_operator_up",
        ),
    ],
    indirect=True,
)
@pytest.mark.s390x
def test_kubevirt_cdi_operator_up(
    prometheus,
    disabled_virt_operator,
    scaled_deployment,
):
    validate_metrics_value(
        prometheus=prometheus,
        expected_value="0",
        metric_name="kubevirt_cdi_operator_up",
    )


@pytest.mark.polarion("CNV-10019")
def test_kubevirt_cdi_import_pods_high_restart(
    prometheus, metric_cdi_import_pods_high_restart_initial_value, created_fake_data_volume_resource
):
    validate_metrics_value(
        prometheus=prometheus,
        metric_name=KUBEVIRT_CDI_IMPORT_PODS_HIGH_RESTART,
        expected_value=str(metric_cdi_import_pods_high_restart_initial_value + 1),
    )
